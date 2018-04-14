
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#创建db之后，要创建模型，而我们的模型全部放在model.py里头,所以我们在创建model.py