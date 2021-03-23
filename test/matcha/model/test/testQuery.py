from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
import matcha.config
import logging

def display(records):
    for record in records:
        print(record)
        print('---------------------------------\n')

if __name__ == "__main__":
    '''
    Define logging LEVEL
    '''
    logging.basicConfig(level=logging.DEBUG)

    '''
    Print Postgresql connection parameters read from 'resources/configuration/config.json' file
    '''
    print('Postgresql', matcha.config.config['postgresql'])

    '''
    select all Connections records with jointure on Users
    '''
    records = DataAccess().fetch('Connection', joins=[('users_id', 'u')])
    display(records)
    print("User:",records[1].users_id)

    '''
    select all Connections records without jointure
    '''
    records = DataAccess().fetch('Connection')
    print("User:",records[1].users_id)

    '''
    select Connections id=12 records with jointure on Users
    '''
    records = DataAccess().fetch('Connection', joins='users_id', conditions='12')
    display(records)

    '''
    select Users whith conditions: gender='Male' and id>2, order by id descending 
    '''
    records = DataAccess().fetch('Users', conditions=[('gender','Male'), ('id', '>', 2)], orderby='1 desc')
    display(records)

    
    '''
    Create users Boris. All needed fields must be specified to avoid error
    '''
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
    DataAccess().persist(users)
    '''
    Check if users.id and users.last_update are defined
    '''
    print(users)
    users.description="Blond, intelligent mais menteur et plus menteur qu'intelligent!"
    DataAccess().merge(users)
    '''
    Check if users.last_update is changed
    '''
    print(users)
    '''
    reinitialize data
    '''
    DataAccess().execute("delete from users where user_name='borisjohnson'")
    DataAccess().execute("alter sequence USERS_ID_SEQ restart with 5")
