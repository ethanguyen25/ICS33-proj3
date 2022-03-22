import re, traceback, keyword


def pnamedtuple(type_name, field_names, mutable = False, defaults = {}):
    def show_listing(s):
        for line_number, line_text in enumerate( s.split('\n'),1 ):  
            print(f' {line_number: >3} {line_text.rstrip()}')
        
    # put your code here
    def unique(iterable):
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i
    
    pattern = "^[a-zA-Z]{1}\w*$"
    if not isinstance(type_name,str) or not isinstance(field_names,(str,list)):
        raise SyntaxError
    if re.match(pattern,type_name) == None:
        raise SyntaxError
    if isinstance(field_names,str):
        asplit = [i for i in unique(re.split('[,\s]',field_names)) if i!='']
        for x in asplit:
            if x in keyword.kwlist:
                raise SyntaxError
        a = [re.match(pattern,i) for i in asplit]
        if None in a:
            raise SyntaxError
    elif isinstance(field_names,list):
        asplit = field_names
        for x in field_names:
            if x in keyword.kwlist:
                raise SyntaxError
        a = [re.match(pattern,i) for i in field_names]
        if None in a:
            raise SyntaxError
    
    dlist = [k for k in defaults]
    for x in dlist:
        if x not in asplit:
            raise SyntaxError
        

        
    
    inits = '\n'.join(['        self.'+i+"="+i for i in asplit])
    aparam = ','.join([i for i in asplit])
    new_line = '\n'
    eight_space = '        '
    getter = ''.join([f"    def get_{i}(self): {new_line}{eight_space}return self.{i}{new_line}" for i in asplit])


    
    # bind class_definition (used below) to the string constructed for the class
    class_template= """\
class {type_name}:
    _fields = {asplit}
    mutable = {mutable}
    
    def __init__(self,{aparam}):
{selfs}
    
    def __repr__(self):
        a = ''
        for i in {asplit}:
            #print(i,'fuck ethan in the sike')
            a+=i+"="+str(self.__dict__[i])+','
        return "{type_name}("+a.rstrip(',')+")"
        
{getter}

    def __getitem__(self,key):
        if isinstance(key,int):
            return self.__dict__[{asplit}[key]]
        else:
            if key not in self.__dict__:raise IndexError
            return self.__dict__[key]
            

    def __eq__(self,joooooooooooon):
        return repr(self) == repr(joooooooooooon)
        
    
    def _asdict(self):
        suckisucki = dict()
        for i in {asplit}:
            suckisucki[i] = self.__dict__[i]
        return suckisucki
    
    
    def _make(args):
        return {type_name}(*args)
        

    def _replace(self,**kargs):
        alist = [self.__getitem__(i) for i in {asplit}]
        
        new_obj = {type_name}._make(alist)
        for i in kargs.keys():
            if i not in {asplit}:
                raise TypeError("fucked")
        for key,value in kargs.items():
            if self.mutable:
                self.__dict__[key] = value
                
            else:        
                new_obj.__dict__[key] = value
        if not self.mutable:
            return new_obj

    
    def __setattr__(self,name,value):
        if name not in self.__dict__:
            self.__dict__[name]=value
        else:
            if not self.mutable:
                raise AttributeError
            else:
                self.__dict__[name]=value
"""
    # For debugging, uncomment next line, which shows source code for the class
    class_definition = \
    class_template.format(type_name=type_name, asplit=asplit, mutable = mutable,
                          aparam=aparam, selfs = inits,getter=getter )
    show_listing(class_definition)

    # Execute the class_definition (a str), in a special name space; then bind
    #   its source_code attribute to class_definition; after try/except return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )      
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):          
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bsc.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
