import re
import argparse
from string import punctuation
from scipy.io import wavfile

import torch
import yaml
import numpy as np
from g2p_en import G2p
from pypinyin import pinyin, Style
import os

from utils.model import get_model, get_vocoder
from utils.tools import to_device, synth_samples
from text import text_to_sequence, vi_number_1, convertBienSoXe


class HandleBSX():
    def __init__(self,configPath):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_config(configPath)      
        self.speakers = np.array([self.speaker_id])
        self.model = get_model(self.restore_step, self.configModels, self.device, train=False)

        self.vocoder = get_vocoder(self.model_config, self.device)
        self.cvBXS = convertBienSoXe.ConvertBSX()

    def load_config(self,configPath):
        self.configs = yaml.load(
            open(configPath, "r"), Loader=yaml.FullLoader
        )
        self.pitch_control=self.configs["control_values"]["pitch_control"]
        self.energy_control=self.configs["control_values"]["energy_control"]
        self.duration_control =self.configs["control_values"]["duration_control"] 


        self.restore_step=self.configs["restore_step"]
        self.speaker_id=self.configs["speaker_id"]


        self.preprocess_config = yaml.load(
            open(self.configs["configModels"]["preprocess_config"], "r"), Loader=yaml.FullLoader
        )
        self.model_config = yaml.load(open(self.configs["configModels"]["model_config"], "r"), Loader=yaml.FullLoader)
        self.train_config = yaml.load(open(self.configs["configModels"]["train_config"], "r"), Loader=yaml.FullLoader)
        self.configModels = (self.preprocess_config, self.model_config, self.train_config)
        
            

    def read_lexicon(self,lex_path):
        lexicon = {}
        with open(lex_path) as f:
            for line in f:
                temp = re.split(r"\s+", line.strip("\n"))
                word = temp[0]
                phones = temp[1:]
                if word.lower() not in lexicon:
                    lexicon[word.lower()] = phones
        return lexicon


    def preprocess_vietnam(self,text):
        text = text.rstrip(punctuation)
        lexicon = self.read_lexicon(self.preprocess_config["path"]["lexicon_path"])

        g2p = G2p()
        phones = []
        text= self.cvBXS .FormatTextBSX(text)
        text = vi_number_1.normalize_number(text)

        words = re.split(r"([,;.\-\?\!\s+])", text)
        for w in words:
            if w.lower() in lexicon:
                phones += lexicon[w.lower()]
            else:
                # check number with sign
                list_number_with_sign = vi_number_1.process_number_sign(w)
                if len(list_number_with_sign) != 0:
                    for number_with_sign in list_number_with_sign:
                        try:
                            read_number_string = vi_number_1.process_number(int(number_with_sign))
                        except ValueError:                        
                            read_number_string = ''
                        numbers_list = re.split(r"([,;.\-\?\!\s+])", read_number_string)
                        for num in numbers_list:
                            if num.lower() in lexicon:
                                phones += lexicon[num.lower()]
                    continue            
                # default
                phones += list(filter(lambda p: p != " ", g2p(w)))

        phones = "{" + "}{".join(phones) + "}"
        phones = re.sub(r"\{[^\w\s]?\}", "{sp}", phones)
        phones = phones.replace("}{", " ")

        print("Raw Text Sequence: {}".format(text))
        print("Phoneme Sequence: {}".format(phones))
        sequence = np.array(
            text_to_sequence(
                phones, self.preprocess_config["preprocessing"]["text"]["text_cleaners"]
            )
        )
        return np.array(sequence)
   

    def synthesize(self, text):
        ids = raw_texts = [text[:100]]
        texts=np.array([self.preprocess_vietnam(text)])
        text_lens = np.array([len(texts[0])])
        batchs = [(ids, raw_texts, self.speakers, texts, text_lens, max(text_lens))]
        for batch in batchs:
            batch = to_device(batch, self.device)
            with torch.no_grad():
                # Forward
                output = self.model(
                    *(batch[2:]),
                    p_control=self.pitch_control,
                    e_control=self.energy_control,
                    d_control=self.duration_control
                )
                wav_prediction, fig =synth_samples(
                    batch,
                    output,
                    self.vocoder,
                    self.model_config,
                    self.preprocess_config,
                    self.train_config["path"]["result_path"],
                )
        pathFile=os.path.join("output/result/viet-tts", "{}.wav".format("basename"))
        wavfile.write(pathFile, 22050, wav_prediction)
        return pathFile
        




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="raw text to synthesize, for single-sentence mode only",
    )
    parser.add_argument(
        "--configPath",
        type=str,
        default='config/config.yaml',
        help="raw text to synthesize, for single-sentence mode only",
    )   
    args = parser.parse_args()

    assert args.text is not None

    handleBSX =HandleBSX(args.configPath)
    
    handleBSX.synthesize(args.text)

