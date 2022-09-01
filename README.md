# Read Plate TTS

## Tải module
	Link tải: https://drive.google.com/drive/folders/1DFP2Hka-9Q1UWxUbG_FJd3HrTh9LaZ7N?usp=sharing

## Yêu cầu: 

   + python 3.6

## Cài đặt các thư viện

```
	pip3 install -r requirements.txt
```



## Chạy Module

### 	Chạy trực tiếp module:

```
##### usage:python3 handleBienSoXe[1-2].py [-h] --text TEXT [--configPath CONFIGPATH]

​	optional arguments:
  	-h, --help                      show this help message and exit

 	 --text TEXT                    raw text to synthesize, for single-sentence mode only

 	 --configPath CONFIGPATH       path file config model 
​	                               Default : "config/config.yaml"`
```



### 	Chạy module với Fastapi

#### Chạy câu lệnh :

```
	python3  server.py
```

#### Truy cập đường dẫn http://127.0.0.1:8080/docs để test thử

