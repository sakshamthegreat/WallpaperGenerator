from PIL import Image, ImageDraw
import requests
import json

def vertical (a, b, c, image):
  pixels = image.load()
  # print("vertical")
  # print(b)
  # print(c)
  rgb_im = image.convert('RGB')
  if(b>c):
    x = b
    b = c
    c = x
  for i in range(b,c):
    # print(a)
    # print(i)
    r, g, b = rgb_im.getpixel((a, i))
    pixels[a, i] = (int((2 * r + 0)/3), int((2 * g + 186)/3), int((2 * b + 255)/3))

#todo: get vertical line rendering working
def line(a, b, c, d, image, x_list, y_list):
  # print(a)
  # print(b)
  # print(c)
  # print(d, end='\n')
  #get image matrix
  pixels = image.load()
  #if vertical, do vertical
  if(a == c):
    vertical(a, b, d, image)
    return
  #calculating slope
  dx = (d-b)/(c-a)
  # print(dx)
  #calclating y intercept
  z = int(b - dx*a)
  #if if points are in reverse, write them in reverse
  if(a > c):
    x = a
    a = c
    c = x
    x = b
    b = d
    d = x
  rgb_im = image.convert('RGB')
  for i in range(a, c):
    
    # pixels[i, z + int(i*dx)] = (0, 186, 255)
    # print(a)
    # print(i)
    r, g, b = rgb_im.getpixel((a, z + int(i*dx)))
    # pixels[a, z + int(i*dx)] = (int((r + 0)/2), int((g + 186)/2), int((b + 255)/2))
    if i in x_list:
      # print("here")
      x_loc = x_list.index(i)
      # print(x_loc)
      y_list[x_loc].append(z + int(i*dx))
    else:
      x_list.append(i)
      y_temp = []
      y_temp.append(z + int(i*dx))
      y_list.append(y_temp)



img = Image.new('RGB', (1920, 1080), color = (255 , 0, 162))


URL = "http://api.noopschallenge.com/polybot"
PARAMS = {'count':40, 'minSides': 3, 'maxSides':15, 'width': 1919, 'height': 1079}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
# print(data)
y = data['polygons']
for j in range(0, len(y)):
  x = y[j]
  x_list = []
  y_list = []
  count = 0
  for i in range(1, len(x)):
    r = x[i-1]['x']
    s = x[i-1]['y']
    t = x[i]['x']
    v = x[i]['y']
    # print(r)
    # print(s)
    # print(t)
    # print(v)
    line(r,s,t,v, img, x_list, y_list)
    r = x[len(x)-1]['x']
    s = x[len(x)-1]['y']
    t = x[0]['x']
    v = x[0]['y']
    # print(r)
    # print(s)
    # print(t)
    # print(v)
    line(r,s,t,v, img, x_list, y_list)
  # print(len(x_list))
  # print(len(y_list))
  for k in range(0, len(x_list)):
    # print(k)
    # print("x: " + str(x_list[k]))
    # print("y: " + str(y_list[k]))
    # print("y: " + str(y_list[i][1]))
    vertical(x_list[k], min(y_list[k]), max(y_list[k]), img)
  # print(x_list)
  # print(y_list)

img.save('pil_text.png')
