from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.FrontEnd.C_Grouper.TabGroupInitializations.TabGroupInitialization import *
from application.FrontEnd.C_Grouper.WidgetGroupInitializations.WidgetGroupInitialization import *
from application.FrontEnd.C_Grouper.SpliterGroupInitializations.SpliterGroupInitialization import *
from application.FrontEnd.D_WindowFolder.WindowInitializations.windowInitialization import *
from application.FrontEnd.E_combiner.connections import *




def ExtentionDebugWindow():
        debugWindow.add_widgets_to_window(
                
                dbug_info,
                dbug_num,
                dbug_btn
            )
        
        debugWindow.show()