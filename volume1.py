from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


dict = {0: -65.25, 1: -56.99, 2: -51.67, 3: -47.74, 4: -44.62, 5: -42.03, 6: -39.82, 7: -37.89, 8: -36.17,
            9: -34.63, 10: -33.24,
            11: -31.96, 12: -30.78, 13: -29.68, 14: -28.66, 15: -27.7, 16: -26.8, 17: -25.95, 18: -25.15, 19: -24.38,
            20: -23.65,
            21: -22.96, 22: -22.3, 23: -21.66, 24: -21.05, 25: -20.46, 26: -19.9, 27: -19.35, 28: -18.82, 29: -18.32,
            30: -17.82,
            31: -17.35, 32: -16.88, 33: -16.44, 34: -16.0, 35: -15.58, 36: -15.16, 37: -14.76, 38: -14.37, 39: -13.99,
            40: -13.62,
            41: -13.26, 42: -12.9, 43: -12.56, 44: -12.22, 45: -11.89, 46: -11.56, 47: -11.24, 48: -10.93, 49: -10.63,
            50: -10.33,
            51: -10.04, 52: -9.75, 53: -9.47, 54: -9.19, 55: -8.92, 56: -8.65, 57: -8.39, 58: -8.13, 59: -7.88,
            60: -7.63,
            61: -7.38, 62: -7.14, 63: -6.9, 64: -6.67, 65: -6.44, 66: -6.21, 67: -5.99, 68: -5.76, 69: -5.55, 70: -5.33,
            71: -5.12, 72: -4.91, 73: -4.71, 74: -4.5, 75: -4.3, 76: -4.11, 77: -3.91, 78: -3.72, 79: -3.53, 80: -3.34,
            81: -3.15, 82: -2.97, 83: -2.79, 84: -2.61, 85: -2.43, 86: -2.26, 87: -2.09, 88: -1.91, 89: -1.75,
            90: -1.58,
            91: -1.41, 92: -1.25, 93: -1.09, 94: -0.93, 95: -0.77, 96: -0.61, 97: -0.46, 98: -0.3, 99: -0.15, 100: 0.0}
#Y = a + b·ln(X) X为0~100， Y为系统中的
#a = -67.2539298150948
#b = 14.3485442547888
#相关系数 R2：0.998887667749056


def vol_transfer(x):
    return dict[x]*96.0/(65.25)

def vl_set(data):
    volume.SetMasterVolumeLevel(vol_transfer(data), None)
    print(f'已设置音量为{data}')
    #设置声音大小

def vl_edit(data):
    a = -67.2539298150948
    b = 14.3485442547888
    vii = volume.GetMasterVolumeLevel()*65.25/96.0  #dict中的value
    vr=math.exp((vii-a)/b)  #对应音量，不准，待在自己电脑上修正
    if(float(data)<-40):  #向上滑，提高音量
        if(vr<90):
            vii=a+b*math.log(vr+3)
        else:
            vii=0.0
    if(float(data)>40):   #向下滑，调低音量
        if(vr>10):
            vii=a+b*math.log(vr-3)
        else:
            vii=-65.25
    volume.SetMasterVolumeLevel(vii*96.0/65.25, None)
    print(f'已设置音量为{math.exp((vii-a)/b)}%')
#存在问题，还是用自己电脑的数据进行拟合比较好，不过初步效果有了

'''
#判断是否静音，mute为1代表是静音，为0代表不是静音
mute = volume.GetMute()
if mute == 1:
    print('当前是静音状态')
else:
    print('当前是非静音状态')
 
#获取音量值，0.0代表最大，-65.25代表最小
vl = volume.GetMasterVolumeLevel()
print(f'{100-(vl/-0.96)}%')

#获取音量范围，我的电脑经测试是(-96.0, 0.0, 0.125)
#第一个应该代表最小值，第二个代表最大值，第三个不知道是干嘛的
#也就是音量从大到小是0.0到-65.25这个范围
vr = volume.GetVolumeRange()
'''