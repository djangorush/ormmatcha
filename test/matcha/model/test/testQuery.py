from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
import matcha.config
import logging

def display(records):
    for record in records:
        print(record)
        print('---------------------------------\n')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    records = DataAccess().fetch('Connection', joins=[('users_id', 'u')])
    display(records)
    print("User:",records[1].users_id)
#    DataAccess.merge(records[1])

    records = DataAccess().fetch('Connection')
    print("User:",records[1].users_id)

    print("========================================================================")
    records = DataAccess().fetch('Connection', joins='users_id', conditions='12')
    display(records)

    records = DataAccess().fetch('Users', conditions=[('gender','Male'), ('id', '>', 2)], orderby='1 desc')
    display(records)

    print('Postgresql', matcha.config.config['postgresql'])
    
    users = records[0]
    users.active = False
    users.confirm = 'Bonjour les mondes'
    DataAccess().merge(users)
    
    users = Users()
    users.first_name = 'Boris'
    users.last_name = 'Johnson'
    users.user_name = 'borisjohnson'
    users.password = 'ElisabethGetOnMyNerves'
    users.description = 'Blond, intelligent mais menteur'
    users.email = 'boris.johnson@england.uk'
    users.active = True
    users.confirm = None
    users.gender = 'Male'
    users.orientation = 'Hetero'
    users.birthday = '1964-06-19'
#    DataAccess().persist(users)
    
    record = DataAccess().find('Users', conditions=('user_name','borisjohnson'))
    if record:
        DataAccess().remove(records[0])
    
