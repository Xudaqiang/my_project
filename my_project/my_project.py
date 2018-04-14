from flask import Flask, render_template, request, redirect, url_for, session
import config

from models import User,Question  #这里导入的User是为了验证User表中的数据，比如一件注册的手机号...
from exts import db  #db要用来初始化app,第17行。

#初始化一个flask对象
#Flask()


#需要传递一个参数__name__
# 1.方便flask框架去寻找资源
# 2.方便flask插件如Flask-Sqlalchemy出现错误的时候，好去寻找问题所在的位置
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)



from decorators import login_required


# “@”开头，并且在函数的上面，说明是装饰器，
# 这个装饰器的作用是做一个url玉视图函数的映射
@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            # 如果有这个用户，我们就要设置一下cookie给前端浏览器，不然下次再进来我还是不知道它是谁
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            # 此时已经登陆成功，让他跳转到首页
            return redirect(url_for('index'))
        else:
            return '手机号码或者密码错误，请确认登录！'

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果被注册就不能被注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机已被注册'
        else:
            # password1要和2相等
            if password1 != password2:
                return '两次密码不相等，请核对后再填写！'
            else:
                user = User(telephone=telephone, username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，跳转到登录页面
                return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/login/')
def logout():
    session.pop('user_id')  #也可以del session['user_id'],还有个最粗暴的session.clear()
    return redirect(url_for('login'))

@app.route('/question/', methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
