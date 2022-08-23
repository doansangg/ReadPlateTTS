#! /bin/bash
python prepare_align ./config/Viet_tts/preprocess.yaml

../montreal-forced-aligner/bin/mfa_train_and_align \
./raw_data/mta/mta0 \
./lexicon/viet-tts-lexicon.txt \
./preprocessed_data/TextGrid \
-o ./align-acoustic-models.zip