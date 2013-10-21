"""
Author: Piotr A. Zolnierczuk (zolnierczukp at ornl dot gov)
 
Based on a paper by:
Drawing an elephant with four complex parameters
Jurgen Mayer, Khaled Khairy, and Jonathon Howard,
Am. J. Phys. 78, 648 (2010), DOI:10.1119/1.3254017


MODIFIED: W. Radigan October 21, 2013
Now includes animation to visualize the "trunk wiggle"

The original paper can be found here:
    http://java-srv1.mpi-cbg.de/publications/getDocument.html?id=ff8080812daff75c012dc1b7bc10000c
    

"""
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt


# elephant parameters
p1, p2, p3, p4 = (50 - 30j, 18 +  8j, 12 - 10j, -15 - 60j )
p5 = 40 + 20j # eyepiece

def fourier(t, C):
    f = np.zeros(t.shape)
    A, B = C.real, C.imag
    for k in range(len(C)):
        f = f + A[k]*np.cos(k*t) + B[k]*np.sin(k*t)
    return f
 
def elephant(t, p1, p2, p3, p4, p5):
    npar = 6
    Cx = np.zeros((npar,), dtype='complex')
    Cy = np.zeros((npar,), dtype='complex')
 
    Cx[1] = p1.real*1j
    Cx[2] = p2.real*1j
    Cx[3] = p3.real
    Cx[5] = p4.real
 
    Cy[1] = p4.imag + p1.imag*1j
    Cy[2] = p2.imag*1j
    Cy[3] = p3.imag*1j
 
    x = np.append(fourier(t,Cx), [-p5.imag])
    y = np.append(fourier(t,Cy), [p5.imag])
 
    return x,y

n_Frames = 30
jnk =0

def wiggle(num,line,jnk):
    global p1,p2,p3,p4,p5
    if num <= n_Frames/2:
        p4 += (.2+0j)
        p5 += (0+.3j)
    else:
        p4 -= (.2+0j)
        p5 -= (0+.3j)
    x, y = elephant(np.linspace(0,2*np.pi,1000), p1, p2, p3, p4, p5)
    line.set_data(y,-x)
    return line,

fig1 = plt.figure()
fig1.set_size_inches(1,1)
l, = plt.plot([], [], 'r.')
plt.xlim(-80, 100)
plt.ylim(-80, 100)
plt.title('Fitting an Elephant')
line_ani = animation.FuncAnimation(fig1, wiggle, n_Frames, fargs=(l,jnk),
    interval=100, blit=False, repeat = False)

plt.show()
line_ani.save("movie.mp4", writer='ffmpeg')

# The animated GIF can be made with FFMPEG directly using the command line:
# C:\Users\WRadigan>ffmpeg -i movie.mp4 -t 5 -s 400x300 out.gif
