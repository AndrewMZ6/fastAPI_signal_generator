# fastAPI_signal_generator
fast api service for getting typical signals  
The application is used to fast get typical OFDM signals for testing purposes remotely  

status of last deployment  <br/>
<img src="https://github.com/AndrewMZ6/fastAPI_signal_generator/actions/workflows/main.yml/badge.svg?branch=main"> <br>

The API provides:		
 - acquire complex ofdm signal
 - make and fast fourier transform of an array

Libs used:
- Numpy
- Commpy
- FastApi (and it's dependencies)
- SQLAlchemy


The planned design of the application is pictuded below   
![Пустой диаграммой (18)](https://github.com/AndrewMZ6/fastAPI_signal_generator/assets/40640833/3d06bd2c-302f-41c8-bc66-12ef490fac86)



## Docker command to build the image:

```
docker build -t myimage .
```   

## Docker command to run the container:

```
docker run -d --name mycontainer -p 8088:8088 myimage
```   
