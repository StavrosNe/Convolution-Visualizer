import customtkinter as ctk
from convolution import Convolution_Signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg , NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter

class Interface(ctk.CTk):
    def __init__(self):

        super().__init__()
         # appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color = '#0D0D0D')

        # title
        self.title('Convolution Integral Visualizer')

        #frame
        self.widgetframe = ctk.CTkFrame(master=self,width=500,height=720,corner_radius=0)
        self.plotframe = ctk.CTkFrame(master=self,width=780,height=720,
                                      corner_radius=0,fg_color='#0D0D0D')

        #widgets
        self.signalentry = ctk.CTkEntry(master=self.widgetframe,
                                    width = 250,height=40,
                                    placeholder_text="Enter Signal",
                                    font=("Roboto",18),corner_radius=10)
                                            
        self.kernelentry = ctk.CTkEntry(master=self.widgetframe,
                                    width = 250,height=40,
                                    placeholder_text="Enter Kernel",
                                    font=("Roboto",18),corner_radius=10)
        
        self.convolutionbutton = ctk.CTkButton(master=self.widgetframe,
                                    width = 60,height=40,
                                    text="Convolution",
                                    font=("Roboto",18),corner_radius=10,
                                    command = self.plot_convolution)

        self.timeslider = ctk.CTkSlider (master = self.widgetframe, from_=1, to=10, 
                                         number_of_steps = 9 ,
                                         command =self.timeslider_command)
        
        self.timelabel = ctk.CTkLabel(master = self.widgetframe, text = 'Δt',
                                      width = 100,height = 40,
                                      font=("Helvetica",20,'bold'))
        
        self.samplingtime_slider = ctk.CTkSlider (master = self.widgetframe, from_=1, to=0.01, 
                                         number_of_steps = 999 ,
                                         command =self.samplingtime_slider_command)
        
        self.samplingtime_label = ctk.CTkLabel(master = self.widgetframe, text = 'Sampling Time',
                                      width = 100,height = 40,
                                      font=("Helvetica",20,'bold'))
        
        self.signal_label = ctk.CTkLabel(master = self.widgetframe, text = 'Signal',
                                      width = 100,height = 40,
                                      font=("Helvetica",20,'bold'))
        
        self.kernel_label = ctk.CTkLabel(master = self.widgetframe, text = 'Kernel',
                                      width = 100,height = 40,
                                      font=("Helvetica",20,'bold'))
        
        self.signalmenu = ctk.CTkOptionMenu(self.widgetframe, values=["Square","Triangle", 
                                          "Unit Step","Damped Sine","Exp","Ramp"],
                                            width = 180 , font=("Roboto",18,),
                                            anchor = 'center',
                                            command = self.signal_menu_set) 
        self.signalmenu.set("Signal")

        self.kernelmenu = ctk.CTkOptionMenu(self.widgetframe, values=["Square","Triangle", 
                                    "Unit Step","Impulse","Exp","Ramp"],
                                      width = 180 , font=("Roboto",18,),
                                            anchor = 'center',
                                            command = self.kernel_menu_set) 
        
        self.kernelmenu.set("Kernel")

        #placement
        self.widgetframe.place(relx = 0 , rely = 0 , anchor = 'nw')
        self.plotframe.place(relx = 1 , rely = 0 , anchor = 'ne')

        self.signal_label.place(relx = 0.5 , rely = 0 , anchor = 'n')
        self.signalentry.place(relx = 0.05 , rely = 0.1 , anchor = 'w')
        self.signalmenu.place(relx = 0.95 , rely = 0.1 , anchor = 'e')

        self.kernel_label.place(relx = 0.5 , rely = 0.2 , anchor = 'center')
        self.kernelentry.place(relx = 0.05 , rely = 0.27 , anchor = 'w')
        self.kernelmenu.place(relx = 0.95 , rely = 0.27 , anchor = 'e')

        self.timelabel.place(relx = 0.5 , rely = 0.6 , anchor = 'center')
        self.timeslider.place(relx = 0.5 , rely = 0.65 , anchor = 'center')

        self.samplingtime_label.place(relx = 0.5 , rely = 0.75 , anchor = 'center')
        self.samplingtime_slider.place(relx = 0.5 , rely = 0.8 , anchor = 'center')

        self.convolutionbutton.place(relx = 0.5 , rely= 0.9 , anchor = 'center')

    def timeslider_command(self,time):
        string = f'Δt : ({-time} , {time})'
        self.timelabel.configure(text=string)

    def samplingtime_slider_command(self,value):
        sampling_time = "{:.2f}".format(value)

        if value == 1:
            string = f'Sampling Time : {sampling_time} second'
        else:
            string = f'Sampling Time : {sampling_time} seconds'
        self.samplingtime_label.configure(text=string)

    def signal_menu_set(self,choice):
        current = self.signalentry.get()
        length = len(current)
        self.signalentry.delete(0,length)
        self.signalentry.insert(0,choice)
    
    def kernel_menu_set(self,choice):
        current = self.kernelentry.get()
        length = len(current)
        self.kernelentry.delete(0,length)
        self.kernelentry.insert(0,choice)

    def convolution(self):

        signal_entry = self.signalentry.get()
        kernel_entry = self.kernelentry.get()
        time = self.timeslider.get()
        samplig_time = float(self.samplingtime_slider.get())
        
        if ',' in signal_entry:
            signal = []
            temp = ''
            for char in signal_entry:
                if char!= ',':
                    temp +=char
                elif char==',':
                    signal.append(temp)
                    temp = ''
            signal.append(signal_entry[-1])
                
        else:
            signal = signal_entry


        if ',' in kernel_entry:
            kernel = []
            temp = ''
            for char in kernel_entry:
                if char!= ',':
                    temp +=char
                elif char==',':
                    kernel.append(temp)
                    temp = ''
            kernel.append(kernel_entry[-1])     
        else:
            kernel = kernel_entry

        convolution = Convolution_Signal(signal,kernel,-time,time,samplig_time)

        return convolution.tvector , convolution.fvector , convolution.gvector , convolution.convolution_signal
    

    def plot_convolution(self):
        # Check if there's an existing canvas in the plotframe
        for widget in self.plotframe.winfo_children():
            widget.destroy()

        list = self.convolution()
        tvector = list[0]
        fvector = list[1]
        gvector = list[2]
        convolution_signal = list[3]

        fig = Figure(figsize=(9.8, 8.6), dpi=100)
        ax1 = fig.add_axes([0.1, 0.7, 0.8, 0.2])  # Left, bottom, width, height of the first subplot
        ax2 = fig.add_axes([0.1, 0.4, 0.8, 0.2])  # Left, bottom, width, height of the second subplot
        ax3 = fig.add_axes([0.1, 0.1, 0.8, 0.2])  # Left, bottom, width, height of the third subplot

        # Add gridlines and labels
        ax1.grid(True)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Magnitude")
        ax1.set_title("Signal")

        ax2.grid(True)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Magnitude")
        ax2.set_title("Kernel")

        ax3.grid(True)
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Magnitude")
        ax3.set_title("Convolution")

        ax1.plot(tvector, fvector) 
        ax2.plot(tvector, gvector)  
        ax3.plot(tvector, convolution_signal)

        canvas = FigureCanvasTkAgg(fig, master=self.plotframe)  # A tk.DrawingArea.
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.plotframe, pack_toolbar=False)
        toolbar.update()


        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        

def main():
    app = Interface()
    #getting screen width and height of display
    ws= app.winfo_screenwidth()
    hs= app.winfo_screenheight()
    # width and height of app
    w = 1280
    h = 720
    # coordiantes on where the app opens
    x = (ws/2) - (w/2)
    y  = (hs/2) - (h/2)
    #setting tkinter window size
    app.geometry('%dx%d+%d+%d' % (w,h,x,y))
    app.maxsize(1280, 720)
    app.resizable(False, False) 
    
    app.mainloop()


if __name__ == '__main__':
    main()