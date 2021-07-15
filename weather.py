from io import BytesIO
import tkinter as tk
import json
import requests
from PIL import ImageTk,Image
from requests.models import Response
import datetime



APPID = "ba011cfa6f5a1ba0d8ec1c3a2868f257"


def write_into_file(data):
    with open('data.json', 'w')as file:
        json.dump(data, file)


def getweather(window):  # this works after clicking button get weather
    
    city = textField.get()
    api_response_url = "https://api.openweathermap.org/data/2.5/weather?q=" +city+"&appid="+APPID
    response = requests.get(api_response_url)
    response_data = response.json()
    write_into_file(response_data)

    # take data from the response
    try:
        #icons api
        icons_url=f"http://openweathermap.org/img/wn/{response_data['weather'][0]['icon']}@2x.png" 
        icons_response=requests.get(icons_url)
        icons_data=icons_response.content
        icons_image=ImageTk.PhotoImage(Image.open(BytesIO(icons_data)))

        #flags api
        flags_url=f"https://www.countryflags.io/{response_data['sys']['country']}/shiny/64.png"
        flags_response=requests.get(flags_url)
        flags_data=flags_response.content
        flags_image=ImageTk.PhotoImage(Image.open(BytesIO(flags_data)))


        condition = response_data['weather'][0]['main']
    #changing background image and reading the image
        bg_image_data=Image.open('./projects/weather_projects/images/'+condition+'.jpg')
        resized_image_data=bg_image_data.resize((800,800),Image.ANTIALIAS)
        bg_image=ImageTk.PhotoImage(resized_image_data)


        temp = response_data['main']['temp']-273
        temp_min = response_data['main']['temp_min']-273
        temp_max = response_data['main']['temp_max']-273
        pressure = response_data['main']['pressure']
        humidity = response_data['main']['humidity']
        wind = response_data['wind']['speed']
        sunrise_unix = response_data['sys']['sunrise']
        sunrise_readable = datetime.datetime.fromtimestamp(sunrise_unix)
        sunset_unix = response_data['sys']['sunset']
        sunset_readable = datetime.datetime.fromtimestamp(sunset_unix)
        final_data = f"{condition}\n{round(temp,3)}°C "
        final_info = f'Min Temp: {round(temp_min,3)}°C \n Max temp: {round(temp_max,3)}°C \
        \n Pressure: {pressure} \n Humidity: {humidity}\nWind: {wind}\n sunrise: {sunrise_readable}\n Sunset: {sunset_readable}'
        label1.config(text=final_data)
        label2.config(text=final_info)
        #image lai haleko
        label3.configure(image=bg_image)
        label3.image=(bg_image)
        icons_label.configure(image=icons_image)
        icons_label.image=(icons_image)
        flags_label.configure(image=flags_image)
        flags_label.image=(flags_image)

    except KeyError:
        label1.config(text=response_data['message'])
        label2.config(text=response_data['cod'])


window = tk.Tk()
window.title("Weather App")
window.geometry("800x800")
bg_image_data=Image.open('./projects/weather_projects/images/bg.jpg')
resized_image_data=bg_image_data.resize((800,800),Image.ANTIALIAS)
bg_image=ImageTk.PhotoImage(resized_image_data)
label3=tk.Label(window,image=bg_image)
label3.place(x=0,y=0)


# textfield added
textField = tk.Entry(window, bg='#fafafa', justify='center',font=('poopins', 35, 'italic'), width=20)
textField.pack(pady=20)

# button added
button = tk.Button(window, text="Get weather")
button.pack()
button.bind('<Button>', getweather)

#icons 
icons_label=tk.Label(window,bg='#afafaf')
icons_label.pack()

# display information
label1 = tk.Label(window, bg='#afafaf',font=('poopins', 16, 'italic'))
label1.pack()
#flags
flags_label=tk.Label(window,bg='#afafaf')
flags_label.pack()

label2 = tk.Label(window, bg='#afafaf',font=('poopins', 16, 'italic'))
label2.pack()



window.mainloop()
