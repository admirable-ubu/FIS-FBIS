from hutia import create_app

"""
Main
"""
if __name__ == "__main__":
    create_app("__main__").run(host='0.0.0.0', debug=True, port=5005)
