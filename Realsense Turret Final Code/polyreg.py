import numpy as np

# FRAME_RATE = 30
# TIME_DELTA = float(1/FRAME_RATE)

class Point:
    """
    Point a super simple struct that just contains a position at time t
    """
    def __init__(self, position):
        """
        Pass in a dictionary to reference points on each dimension,
        ex. Point({'x':1, 'y':0, 'z':5})
        Point.coordinates['x'] -> 1
        OR pass in a list or tuple to reference the points as a1,a2,a3...
        ex. Point( (1, 0, 5) )
        Point.coordinates['a1'] -> 1

        """

        self.coordinates = {}
        if type(position) == tuple or type(position) == list:
            n = 0
            for p in position:
                self.coordinates['a'+str(n)] = p
                n += 1
        elif type(position) == dict:
            for label,value in position.items():
                self.coordinates[label] = value


        #self.x = x
        #self.y = y
        #self.t = t
"""
        self.all_x = []
        self.all_y = []
        self.all_t = []
        for p_i in self.p_set:
            self.all_x.append(p_i.x)
            self.all_y.append(p_i.y)
            self.all_t.append(p_i.t)
"""

class Points:
    """
    Points will store a set of the Point object and acts 
    like a container to simplify accessing and storing many Points
    """
    def __init__(self, p_set):
        self.p_set = p_set
        self.len = len(p_set)

        self.labels = []
        for p in self.p_set:
            self.labels = p.coordinates.keys()

        


    
    def all_line(self, label:str) -> list:
        """
        Gets all the points in the line label.
        ex. all_line('x') gives a list of all the points on the x line
        """

        if label not in self.labels:
            return False
        line = []
        for p in self.p_set:
            line.append(p.coordinates[label])
        return line


    def add_point(self, pt):
        self.p_set.append(pt)
        self.len = len(self.p_set)
        for label in pt.coordinates.keys():
            if label not in self.labels:
                self.labels.append(label)

    def pop(self, i=None):
        if i == None:
            pop_point = self.p_set.pop()
        else:
            pop_point = self.p_set.pop(i)
        self.len = len(self.p_set)
        return pop_point
    
    def rm_point(self, pt):
        if type(pt) != Point and (type(pt) == list or type(pt) == tuple):
           pt1 = Point(pt) 
        else:
            pt1 = pt


        for idx,p in enumerate(self.p_set):
            if p == pt1:
                del self.p_set[idx]
                self.len = len(self.p_set)
                return True
        
        return False


    


class PolyReg:
    """
    PolyReg will initialize with a Points object and base its calculations
    off that set of points. PolyReg is helpful for calculating polynomial regression
    based of a set of points over time.
    """
    def __init__(self, points_set):

        # The set of points to use in the polynomial regression
        # Usually this is coordinates from the frames in a second from a camera
        self.points = points_set
        self.prediction = None

    def regress(self, degree=2):
        """
        PolyReg.regress(self, degree=2) is a polynomial regression function that 
        makes 2 regression functions: The first from 0 to t-1, and the second from 1 to t.
        Then, the functions are computed up to t + 1 so that it can be used to later
        predict where the next position could be.
        """

        # This *should* usually be equal to FRAME_RATE
        L = self.points.len

        # coefficients for both of the regression functions
        #
        # The first coef will do a polyfit with L - 1 points from 0 to L - 1
        # and the second will do a polyfit with L - 1 points from 1 to L

        #coefs_1 = np.polyfit(self.points.all_x[0:L-1],
        #                   self.points.all_y[0:L-1],
        #                   degree
        #                   )
        #coefs_2 = np.polyfit(self.points.all_x[1:L],
        #                   self.points.all_y[1:L],
        #                   degree
        #                   )

        y_coefs_1 = np.polyfit(self.points.all_t[0:L-1],
                            self.points.all_y[0:L-1],
                            degree
                            )

        y_coefs_2 = np.polyfit(self.points.all_t[1:L],
                            self.points.all_y[1:L],
                            degree
                            )

        x_coefs_1 = np.polyfit(self.points.all_t[0:L-1],
                            self.points.all_x[0:L-1],
                            degree
                            )
        x_coefs_2 = np.polyfit(self.points.all_t[1:L],
                            self.points.all_x[1:L],
                            degree
                            )


        # The model for the x needs to calculate up to t + 1
        # so this will be a size of amount of points L plus the next time L + 1
        #x_model = np.array(self.points.all_x + [L + 1])
        time_t = np.array(self.points.all_t + [L + 1])

        self.x_model_1 = np.polyval(x_coefs_1, time_t)
        self.x_model_2 = np.polyval(x_coefs_2, time_t)

        self.y_model_1 = np.polyval(y_coefs_1, time_t)
        self.y_model_2 = np.polyval(y_coefs_2, time_t)

        self.x_reg1 = (time_t, self.x_model_1)
        self.x_reg2 = (time_t, self.x_model_2)
    
        self.y_reg1 = (time_t, self.y_model_1)
        self.y_reg2 = (time_t, self.y_model_2)

        self.reg1 = (self.x_model_1, self.y_model_1)
        self.reg2 = (self.x_model_2, self.y_model_2)

    #get the new, predicted point at t+1 based on the projection of the points
    def get_prediction(self):
        """
        Using the models for the y positions, this gets a projection based off
        of the two models, and calculates a predicted position projected off of the
        second regression function. It returns the position and stores it in
        a variable self.prediction
        """
        # Use the derived formula 2*Quad_2(t+1) - Quad_1(t+1)
        # to get the predicted point at time t + 1

        next_time = self.points.len + 1

        if self.prediction != None:
            return self.prediction

        y_Quad_2 = self.y_model_2[-1]
        y_Quad_1 = self.y_model_1[-1]
        x_Quad_2 = self.x_model_2[-1]
        x_Quad_1 = self.x_model_1[-1]

        self.prediction = Point(2*x_Quad_2 - x_Quad_1, 2*y_Quad_2 - y_Quad_1, next_time)

        return self.prediction


                          

