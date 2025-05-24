from datetime import datetime


# 正误反馈板块
def p_correct():
    return True

def p_wrong():
    return False

# 接受用户输入的密码板块
def get_input_password():
    input_password = input("请输入密码：")
    return input_password

# 检查密码是否正确的板块
def check(password,input_password):
    
    if password == input_password:
        return p_correct()
    else:
        return p_wrong()
    
    # return password

class PasswordChecker:
    def __init__(self):
        self.current_time = datetime.now()
        self.hour = self.current_time.hour
        self.month = hex(self.current_time.month)[2:]
        self.date = self.current_time.strftime("%Y%m%d")  # 8位年月日
        self.dow = int(self.current_time.strftime("%w"))  # 当日星期（0=周日，1=周一，...，6=周六）
        # 汇集函数
        self.strategies = [self.get_strategy(i) for i in range(1, 12 + 1)] # 总函数数量在这里设置

    def get_strategy(self, i):
        # 占位用
        # 尝试从类的局部作用域中获取策略函数
        return getattr(self, f"strategy_{i}", self.strategy_11)

    def strategy(self,x,user_defined,entered):          
            if 1 <= x <= len(self.strategies):
               return self.strategies[x- 1](user_defined,entered)  # 调用对应的函数


    def strategy_1(self,user_defined,entered):
        # 日期码乘自定义实数
        return check(int(self.date) * user_defined, int(entered))

    def strategy_2(self,user_defined,entered):
        # 若Dow为奇数，则取Date的奇数位。若Dow为偶数，则取Date的偶数位。在末尾连接Dow
        if self.dow % 2 == 0:  # Dow为偶数
            selected_date = self.date[1::2]  # 取Date的偶数位
        else:  # Dow为奇数
            selected_date = self.date[::2]  # 取Date的奇数位
        return check(selected_date + str(self.dow), entered)

    def strategy_3(self,user_defined,entered):
        # Hour×_________（用户自定义实数）
        return check(int(self.hour) * user_defined, int(entered))

    def strategy_4(self,user_defined,entered):
        # 若Hour为奇数，则取Date的奇数位.若Hour为偶数，则取Date的偶数位.在末尾连接Hour
        if self.hour % 2 == 0:  # Dow为偶数
            selected_date = self.date[1::2]  # 取Date的偶数位
        else:  # Dow为奇数
            selected_date = self.date[::2]  # 取Date的奇数位
        return check(selected_date + str(self.hour), entered)

    def strategy_5(self,user_defined,entered):
        # Hour×Dow
        return check(int(self.hour) * self.dow, int(entered))

    def strategy_6(self,user_defined,entered):
        """
        判断（包含且只包含Hour个Month字符的任意字符串）
        """
        # 判断出现次数是否等于当前小时数
        return check(entered.count(self.month), self.hour)

    def strategy_7(self,user_defined,entered):
        # 判断（包含且只包含_________（用户自定义实数）个Month字符的任意字符串）
        return check(entered.count(self.month), user_defined)


    def strategy_8(self,user_defined,entered):
        # 判断（包含且只包含Hour个_________（用户自定义1位字符）的任意字符串）
        return check(entered.count(user_defined[0]), self.hour)

    def strategy_9(self,user_defined,entered):
        # 判断（包含且只包含Hour个大写英文字母的任意字符串）
        return check(sum(1 for char in entered if char.isupper()), self.hour)

    def strategy_10(self,user_defined,entered):
        # 判断（包含且只包含_________（用户自定义实数）个大写英文字母的任意字符串）
        return check(sum(1 for char in entered if char.isupper()), user_defined)

    def strategy_11(self,user_defined,entered):
        """
        判断（密码中所有数字类字符加和=Hour（其余字符均不影响））
        """
        return check(sum(int(char) for char in entered if char.isdigit()), self.hour)
    def strategy_12(self,user_defined,entered):
        # 判断（密码中所有数字类字符加和=_________（用户自定义实数））
        return check(sum(int(char) for char in entered if char.isdigit()), user_defined)
