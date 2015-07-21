# Created by cxy on 2014-12-25
# -*- coding: utf-8 -*-
from app import app
from app.views import views, admin


if __name__ == '__main__':
    app.run(debug=True)