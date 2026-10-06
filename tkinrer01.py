# tkiner 모듈 가져오는 코드
import tkinter

#pillow 라이브러리에서 이미지 조작 기능 가져오는 코드
import PIL.Image

#pillow 라이브러리에서 tkinter 변환 기능 가져오기
import PIL.ImageTk



#메인창 객체 생성
root = tkinter.Tk()

#창 제목 설정 (string: 표시할 제목 문자열)
root.title("이미지 다중 배치 및 변형 프로그램")

#창 크기 설정 (string: "가로X세로" 픽셀)
root.geometry("600x500")

#자유로운 배치를 위한 canvas 위젯 생성 (root: 부모창, width: 가로 픽셀, height:세로 픽셀, bg:배경색)
canvas = tkinter.Canvas(root, width=600, height=500, bg="white")

#Canvas를 화면에 꽉 채워 배치 (fill: 채울 방향, expand: 창 크기 변경 시 확장 여부)
canvas.pack(fill="both", expand=True)

#Canvas에 택스트 생성 (300: x좌표, 30: Y좌표 text: 출력할 글짜, font: (글꼴,크기 스타일))
canvas.create_text(300, 30, text="이미지 크기 조절 및 회전 예시", font=("Arial", 14, "bold"))



#GUI 창이 닫힐때까지 이벤트 루프 지속 실행
root.mainloop()