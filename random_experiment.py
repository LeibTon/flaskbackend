import numpy as np

class Experiment():
    def __init__(self, random, r = 20,part = 5):
        self.random_number = random
        self.r_num = int(r)
        self.part = int(part)
    def char2array(self,s):
        m = [int(c) for c in s if int(c) in [0,1]]
        x= np.array(m)
        return x*2-1
    def build_time_matrices(self,x,r):
        x1 = np.ones(len(x)-r)
        x1 = np.vstack((x1, x[0:-r]))
        xprime = x
        for i in range(r-1):
            xprime = np.roll(xprime, -1)
            x1 = np.vstack((x1, xprime[0:-r]))
        x2 = x[r:]
        return x1, x2
    def AR_model(self,x,r):
        x1,x2 = self.build_time_matrices(x,r)
        p,res,rnk,s = np.linalg.lstsq(x1.T,x2,rcond=None)
        return x1,x2,p
    def AR_predictions(self,x_test,p):
        x1,x2 = self.build_time_matrices(x_test,len(p)-1)
        return np.sign(np.dot(x1.T,p))
    def error_rate(self,x_test,p):
        x1,x2 = self.build_time_matrices(x_test,len(p)-1)
        return np.count_nonzero(x2 - self.AR_predictions(x_test, p)) / len(x2)
    def main(self):
        result_final = {}
        r = np.arange(1, self.r_num)
        x_input = self.random_number
        result_final['input_original'] = [int(c) for c in x_input if c in ['0','1']]
        result_final['input_length'] = len(x_input)
        test_range = len(x_input) - (len(x_input)//self.part if len(x_input)//self.part > 25 else 25)
        result_final['train_length'] = test_range
        x_input_train = x_input[:test_range]
        x_input_test = x_input[test_range:]
        x_random = np.random.randint(2, size=len(x_input))
        result_final['random_original'] = [int(i) for i in list(x_random)]
        x_random_train = x_random[:test_range]
        x_random_test = x_random[test_range:]
        x_train = self.char2array(x_input_train)
        x_test = self.char2array(x_input_test)
        random_train = self.char2array(x_random_train)
        random_test = self.char2array(x_random_test)
        result_final['input_train'] = [int(i) for i in list(x_train)]
        result_final['input_test'] = [int(i) for i in list(x_test)]
        result_final['random_train'] = [int(i) for i in list(random_train)]
        result_final['random_test'] = [int(i) for i in list(random_test)]
        result_final['r-values'] = [int(i) for i in list(r)]
        temp = []
        for i, rr in enumerate(r):
            temp_dict = {}
            # fitting the model on training data
            x1, x2, p = self.AR_model(x_train, rr)
            temp_dict['r-value'] = int(rr)
            temp_dict['input_p'] = [float(i) for i in list(p)]
            x_1,x_2,p_ = self.AR_model(random_train,rr)
            temp_dict['random_p'] = [float(i) for i in list(p)]
            # computing and storing the test error
            test_error = self.error_rate(x_train, p)
            temp_dict['input_train_error'] = float(test_error)
            test_error = self.error_rate(x_test, p)
            temp_dict['input_test_error'] = float(test_error)
            test_error = self.error_rate(random_train, p_)
            temp_dict['random_train_error'] = float(test_error)
            test_error = self.error_rate(random_test, p_)
            temp_dict['random_test_error'] = float(test_error)
            temp.append(temp_dict)
        result_final['training_part'] = temp
        return result_final


#000100101010101010101001010101001001101010101010101010101001001010101010101010010110000000101010101010010101011010101011110101010101010101010010101001010010101001010011001010100101010010
