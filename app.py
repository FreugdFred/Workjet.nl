from website import app
import sys
sys.dont_write_bytecode = True

# import os
# os.system('color')


if __name__ == '__main__':
    app.run()

    # faq in plaats van werkgever werknemer
    # gunicorn -w 4 -b 0.0.0.0 'website.app:create_flask()'

    # sudo kill -9 `sudo lsof -t -i:5000`
