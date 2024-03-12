import numpy as np
from points import Point, Points

# FRAME_RATE = 30
# TIME_DELTA = float(1/FRAME_RATE)


def regress(pts:Points, degree=2):
    """
    This function assumes pts is a class Points containing points with a dimension of 2 and a time t
    """
    """
    Need the coefficients from 0 to t-1 and from 1 to t.
    This will produce two polynomials fitted from the positions which will be used to 
    get a prediction

    The coefs will be stored as such: {"x":(poly1, poly2), "y":(poly1, poly2) ... "n":(poly1, poly2)}
    """
    if len(pts.keys()) != 2:
        raise ValueError
    coefs = dict()
    k1 = pts.keys()[0]
    k2 = pts.keys()[1]
    time = pts._time
    t1 = time[0:len(time)-1]
    t2 = time[1:len(time)]
    coefs[k1] = (
            np.polyfit(
                t1,
                pts[k1][0:len(pts)-1],
                degree
                ),
            np.polyfit(
                t2,
                pts[k1][1:len(pts)],
                degree
                )
            )
    coefs[k2] = (
            np.polyfit(
                t1,
                pts[k2][0:len(pts)-1],
                degree
                ),
            np.polyfit(
                t2,
                pts[k2][1:len(pts)],
                degree
                )
            )

    model_time = np.array(time + [time[-1]+1])
    model_k1 = (
            np.polyval(coefs[k1][0], model_time),
            np.polyval(coefs[k1][1], model_time)
            )
    model_k2 = (
            np.polyval(coefs[k2][0], model_time),
            np.polyval(coefs[k2][1], model_time)
            )
    print(model_k1)
    print(model_k2)
    print(coefs[k1])
    print(coefs[k2])
    
    return {'mk1': model_k1, 'mk2': model_k2, 'k1':k1, 'k2':k2, 'len': len(time), 'time': time}

def estimate(model):
    next_time = model['time'][-1] + 1


    y_Quad_2 = model['mk2'][1][-1]
    y_Quad_1 = model['mk2'][0][-1]
    x_Quad_2 = model['mk1'][1][-1]
    x_Quad_1 = model['mk1'][0][-1]
    prediction = Point(
            {
            model['k1']:2*x_Quad_2 - x_Quad_1,
            model['k2']:2*y_Quad_2 - y_Quad_1
            },
        next_time
        )

    return prediction







"""
This needs to be updated and is now unusuable with the new 
changes to Point and Points.
"""


#class PolyReg:
#    """
##    PolyReg will initialize with a Points object and base its calculations
##    off that set of points. PolyReg is helpful for calculating polynomial regression
##    based of a set of points over time.
##    """
##    def __init__(self, points_set):
##
##        # The set of points to use in the polynomial regression
##        # Usually this is coordinates from the frames in a second from a camera
##        self.points = points_set
##        self.prediction = None
##
##    def regress(self, degree=2):
##        """
##        PolyReg.regress(self, degree=2) is a polynomial regression function that 
##        makes 2 regression functions: The first from 0 to t-1, and the second from 1 to t.
##        Then, the functions are computed up to t + 1 so that it can be used to later
##        predict where the next position could be.
##        """
##
##        # This *should* usually be equal to FRAME_RATE
##        L = self.points.len
##
##        # coefficients for both of the regression functions
##        #
##        # The first coef will do a polyfit with L - 1 points from 0 to L - 1
##        # and the second will do a polyfit with L - 1 points from 1 to L
##
##        #coefs_1 = np.polyfit(self.points.all_x[0:L-1],
##        #                   self.points.all_y[0:L-1],
##        #                   degree
##        #                   )
##        #coefs_2 = np.polyfit(self.points.all_x[1:L],
##        #                   self.points.all_y[1:L],
##        #                   degree
##        #                   )
##
##        y_coefs_1 = np.polyfit(self.points.all_t[0:L-1],
##                            self.points.all_y[0:L-1],
##                            degree
##                            )
##
##        y_coefs_2 = np.polyfit(self.points.all_t[1:L],
##                            self.points.all_y[1:L],
##                            degree
##                            )
##
##        x_coefs_1 = np.polyfit(self.points.all_t[0:L-1],
##                            self.points.all_x[0:L-1],
##                            degree
##                            )
##        x_coefs_2 = np.polyfit(self.points.all_t[1:L],
##                            self.points.all_x[1:L],
##                            degree
##                            )
##
##
##        # The model for the x needs to calculate up to t + 1
##        # so this will be a size of amount of points L plus the next time L + 1
##        #x_model = np.array(self.points.all_x + [L + 1])
##        time_t = np.array(self.points.all_t + [L + 1])
##
##        self.x_model_1 = np.polyval(x_coefs_1, time_t)
##        self.x_model_2 = np.polyval(x_coefs_2, time_t)
##
##        self.y_model_1 = np.polyval(y_coefs_1, time_t)
##        self.y_model_2 = np.polyval(y_coefs_2, time_t)
##
##        self.x_reg1 = (time_t, self.x_model_1)
##        self.x_reg2 = (time_t, self.x_model_2)
##    
##        self.y_reg1 = (time_t, self.y_model_1)
##        self.y_reg2 = (time_t, self.y_model_2)
##
##        self.reg1 = (self.x_model_1, self.y_model_1)
##        self.reg2 = (self.x_model_2, self.y_model_2)
##
##    #get the new, predicted point at t+1 based on the projection of the points
##    def get_prediction(self):
##        """
##        Using the models for the y positions, this gets a projection based off
##        of the two models, and calculates a predicted position projected off of the
##        second regression function. It returns the position and stores it in
##        a variable self.prediction
##        """
##        # Use the derived formula 2*Quad_2(t+1) - Quad_1(t+1)
##        # to get the predicted point at time t + 1
##
##        next_time = self.points.len + 1
##
##        if self.prediction != None:
##            return self.prediction
##
##        y_Quad_2 = self.y_model_2[-1]
##        y_Quad_1 = self.y_model_1[-1]
##        x_Quad_2 = self.x_model_2[-1]
##        x_Quad_1 = self.x_model_1[-1]
##
##        self.prediction = Point(2*x_Quad_2 - x_Quad_1, 2*y_Quad_2 - y_Quad_1, next_time)
##
#        return self.prediction


