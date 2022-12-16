import sys, os, re

# substitutions : \ vaut ¶
di = { "(.+)¶begin{document}(.+)¶end{document}" : "<body>\g<2></body>", #OK
        r"(.*)\${2}([^\$]*)\${2}(.*)" : "\g<1>¶[\g<2>¶]\g<3>", #OK math mode (display)
        r"(.*)\${1}([^\$]*)\${1}(.*)" : "\g<1>¶(\g<2>¶)\g<3>", #OK math mode
        r"(.*)¶e\^(.*)" : "\g<1>¶rm{e}^\g<2>", #OK exp
        r"(.*)(\d),¶!(\d)(.*)" : "\g<1>\g<2>{,}\g<3>\g<4>", #OK , nbre dec
        r"(.*)¶¶(.*)" : "\g<1><br>\g<2>", #~OK sauf math mode 
        r"(.*)¶par(.*)" : "\g<1><br>\g<2>", #OK
        r"(.*)¶item(.*)" : "\g<1>  </li>ŒŒŒ  <li>\g<2>", #OK
        r"(.*)¶begin\{enumerate\}([^<]*)</li>(.*)¶end\{enumerate\}(.*)" : "\g<1><ol>\g<3></ol>\g<4>",
        r"(.*)¶begin\{itemize\}([^<]*)</li>(.*)¶end\{itemize\}(.*)" : "\g<1><ul>\g<3></ul>\g<4>",
        r"(.*)¶begin\{center\}(.*)¶end\{center\}(.*)" : "\g<1><div class=\"center\">\g<2></div>\g<3>",
        r"(.*)¶begin\{multicols\}\{[0-9]\}(.*)¶end\{multicols\}(.*)" : "\g<1>\g<2>\g<3>",
        r"(.*)¶emph\{([^}]*)\}(.*)" : "\g<1>\g<2>\g<3>",
        r"(.*)¶underline\{([^}]*)\}(.*)" : "\g<1><b>\g<2></b>\g<3>",
        r"(.*)¶textbf\{([^}]*)\}(.*)" : "\g<1><b>\g<2></b>\g<3>",
        r"(.*)¶texttt\{([^}]*)\}(.*)" : "\g<1><code>\g<2></code>\g<3>",
        r"(.*)¶fbox\{([^}]*)\}(.*)" : "\g<1><span class=\"surl\">\g<2></span>\g<3>",
        r"(.*)¶section\{([^}]*)\}(.*)" : "\g<1><h2 class=\"section\">\g<2></h2>\g<3>",
        r"(.*)¶section\*\{([^}]*)\}(.*)" : "\g<1><h2 class=\"section-nocounter\">\g<2></h2>\g<3>",
        r"(.*)¶subsection\{([^}]*)\}(.*)" : "\g<1><h3 class=\"subsection\">\g<2></h3>\g<3>",
        r"(.*)¶subsection\*\{([^}]*)\}(.*)" : "\g<1><h3 class=\"subsection-nocounter\">\g<2></h3>\g<3>",
        r"(.*)¶subsubsection\{([^}]*)\}(.*)" : "\g<1><h4 class=\"subsubsection\">\g<2></h4>\g<3>",
        r"(.*)¶subsubsection\*\{([^}]*)\}(.*)" : "\g<1><h4 class=\"subsubsection-nocounter\">\g<2></h4>\g<3>",
        r"(.*)¶includegraphics\[(.*)\]\{([^}]*)\}(.*)" : "\g<1><img src=\"assets/\g<3>\"/>\g<4>",
        r"(.*)¶exo\{([^}]*)\}(.*)" : "\g<1><div class=\"exo\">\g<2></div>\g<3>",
        r"(.*)¶exo(.*)" : "\g<1>ŒŒŒ<div class=\"exo\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶rema\{([^}]*)\}(.*)" : "\g<1><div class=\"rema\">\g<2></div>\g<3>",
        r"(.*)¶rema(.*)" : "\g<1>ŒŒŒ<div class=\"rema\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶prop\{([^}]*)\}(.*)" : "\g<1><div class=\"prop\">\g<2></div>\g<3>",
        r"(.*)¶prop(.*)" : "\g<1>ŒŒŒ<div class=\"prop\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶theo\{([^}]*)\}(.*)" : "\g<1><div class=\"theo\">\g<2></div>\g<3>",
        r"(.*)¶theo(.*)" : "\g<1>ŒŒŒ<div class=\"theo\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶demo\{([^}]*)\}(.*)" : "\g<1><div class=\"demo\">\g<2></div>\g<3>",
        r"(.*)¶demo(.*)" : "\g<1>ŒŒŒ<div class=\"demo\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶defi\{([^}]*)\}(.*)" : "\g<1><div class=\"defi\">\g<2></div>\g<3>",
        r"(.*)¶defi(.*)" : "\g<1>ŒŒŒ<div class=\"defi\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶meth\{([^}]*)\}(.*)" : "\g<1><div class=\"meth\">\g<2></div>\g<3>",
        r"(.*)¶meth(.*)" : "\g<1>ŒŒŒ<div class=\"meth\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)¶exem\{([^}]*)\}(.*)" : "\g<1><div class=\"exem\">\g<2></div>\g<3>",
        r"(.*)¶exem(.*)" : "\g<1>ŒŒŒ<div class=\"exem\">ŒŒŒ!!!!!!</div>ŒŒŒ\g<2>",
        r"(.*)\{¶color\{([^}]*)\}(.*)" : "\g<1>\g<3>",
        }


def open_text(filename:str) -> str :
    with open(filename) as file :
        st = str(file.read())
        print("OPEN TEXT : ", st)
        return st

def write_text(filename:str, st:str) :
    with open(filename, 'w') as file :
        file.write(st)

def traitement(st:str, di:dict) -> str :
    st = st.replace('\\', '¶')
    #st = st.replace('$', '\\$')
    st = st.replace('\n', 'ŒŒŒ')
    for pattern, repl in di.items() :
        while re.match(pattern, st) :
            print("MATCH : ", pattern)
            st = re.sub(pattern, repl, st, flags=re.DOTALL)
    st = st.replace('¶', '\\')
    st = st.replace('ŒŒŒ', '\n')
    return st

def traite_fichier(filename:str, di:dict, display:bool=False) -> str :
    st = open_text(filename)
    os.system('cls' if os.name == 'nt' else 'clear')
    input(f"Convert {filename} : Press enter")
    st = traitement(st, di)
    print(st)
    return st

if __name__ == "__main__" :
    MAINROOT = "."
    EXTENSIONS = [".tex"]
    INPUT = "input"        
    OUTPUT = "output"      
    DISPLAY = True         # affiche le nom des fichiers traités 1 à 1
    try :
        os.makedirs(os.path.join(MAINROOT, OUTPUT), exist_ok=True)
    except Exception as e :
        print(f"Exception : {e}")
    if len(sys.argv)>1 :               # les fichiers à traiter sont en argument
        filenames = sys.argv[1:]
    else :                             # sinon tous les fichiers .tex sont traités
        filenames = [el for el in os.listdir(os.path.join(MAINROOT, INPUT)) if el[-4:] in EXTENSIONS]
    for filename in filenames :
        st = traite_fichier(os.path.join(MAINROOT, INPUT, filename), di, display=DISPLAY)
        print(st)
        write_text(os.path.join(MAINROOT, OUTPUT, f"{filename[:-4]}.html"), st)

