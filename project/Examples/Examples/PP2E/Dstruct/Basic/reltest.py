from rset import RSet

def test():
    a = RSet( 
            [{'name':'marv',  'job':'engineer'},     
             {'name':'andy',  'job':'engineer'},     
             {'name':'sam',   'job':'manager'},      
             {'name':'mary',  'job':'prez'},         
             {'name':'mira',  'job':'architect'},   
             {'name':'john',  'job':'engineer'},     
             {'name':'eddy',  'job':'administrator'} 
            ])
    
    b = RSet( 
            [{'job':'engineer', 'pay':(25000,60000)},  
             {'job':'manager',  'pay':(50000,'XXX')},  
             {'job':'architect','pay':None},           
             {'job':'prez',     'pay':'see figure 1'}  
            ])

    c = RSet( 
            [{'name':'marv',  'job':'engineer'},     
             {'name':'andy',  'job':'engineer'},     
             {'name':'sam',   'job':'manager'},      
             {'name':'julie', 'job':'engineer'},     
             {'name':'steve', 'job':'manager'}       
            ])

    a.list()
    a.select('job', 'engineer').list()
    a.join(b, 'job').list()

    a.project(['job']).list()      
    a.select('job', 'engineer').project(['name']).list()

    a.find('job', '>', 'engineer').list()
    c.find('job', '!=', 'engineer').list()
    a.bagof("X['name'][0] == 'm'").list()   
    a.bagof("X['job'] > 'engineer'").list()
    a.bagof("X['job'] > 'engineer' or X['name'] == 'eddy'").list()

    a.project(['job']).difference(b.project(['job'])).list()
    a.join(b, 'job').project(['name', 'pay']).list()
    a.select('name','sam').join(b,'job').project(['name', 'pay']).list()
    
test() 
