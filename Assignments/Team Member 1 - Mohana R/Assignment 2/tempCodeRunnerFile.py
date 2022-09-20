# @app.route('/deluser')
# def delete_user(key):
#     connie = sqlite3.connect(db_locale)
#     c = connie.cursor()
#     sql_delete_string = 'DELETE FROM auth WHERE auth.email == (?)'
#     c.execute(sql_delete_string,key)
#     connie.commit()
#     connie.close()
#     return render_template('signup.html')
