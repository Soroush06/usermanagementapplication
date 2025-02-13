from PresentationLayer.Frames.change_role import RoleFrame
from PresentationLayer.window import Window
from PresentationLayer.Frames.login import LoginFrame
from PresentationLayer.Frames.home import HomeFrame
from PresentationLayer.Frames.register import RegisterFrame
from PresentationLayer.Frames.user_management import UserManagementFrame
from ttkbootstrap import Window
from CommonLayer.Decorators.Performance_logger import performance_logger_decorator


class MainView:
    def __init__(self):
        self.frames = {}
        self.window = Window(title="User Management Application",iconphoto="download.png",themename="darkly")

        self.add_frame("usermanagement", UserManagementFrame(self.window, self))
        self.add_frame("change_role", RoleFrame(self.window, self))
        self.add_frame("register", RegisterFrame(self.window, self))
        self.add_frame("home", HomeFrame(self.window, self))
        self.add_frame("login", LoginFrame(self.window, self))

        self.window.mainloop()

    @performance_logger_decorator("MainView")
    def add_frame(self, name, frame):
        self.frames[name] = frame
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    @performance_logger_decorator("MainView")
    def switch_frame(self, frame_name,*args,**kwargs):
        frame = self.frames[frame_name]
        if hasattr(frame,"initialize"):
            frame.initialize(*args,**kwargs)
        frame.tkraise()
        return frame




