FROM python:3.8

WORKDIR /usr/src/mouse
COPY . /usr/src/mouse

RUN pip install mediapipe
RUN pip install opencv
RUN pip install time
RUN pip install autopy
RUN pip install pyautogui

CMD ["python", "/AiVirtualMouseProject.py"]
