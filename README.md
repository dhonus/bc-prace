# Bakalářská práce
# Nástroj pro dokazování platnosti úsudků pomocí Vennových diagramů

Cílem práce je naimplementovat nástroj pro podporu dokazování platnosti úsudků v predikátové logice 1. řádu (PL1) za pomocí Vennových diagramů.

### Práce bude obsahovat:
1. Teorii PL1.
3. Teorii dokazování platnosti úsudků a tautologičnosti formulí v PL1.
4. Analýzu, návrh a implementaci systému pro dokazování platnosti úsudků pomocí Vennových diagramů.

### Literatura
[1] Vopěnka, P.: Úvod do klasické teorie množin, Fragment 2015, ISBN: 978-80-253-1251-3  
[2] Švejdar, V.: Logika - neúplnost, složitost a nutnost, Academia Prague 2002, ISBN: 978-80-200-1005-6  
[3] Duží, M.: Logika pro informatiky, Skripta VŠB-TU Ostrava, 2012


    RECURSIVE DESCENT PARSING
        https://www.youtube.com/watch?v=SToUyjAsaFk
        https://www.codeproject.com/Articles/318667/Mathematical-Expression-Parser-Using-Recursive-Des
        https://en.wikipedia.org/wiki/Recursive_descent_parser
    REMOVING LEFT RECURSION FORMULA
        https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node8.html
    LOGIC
        https://en.wikipedia.org/wiki/Logical_biconditional

    SYMBOLS:        PRECEDENCE
        NOT:    !   1
        AND:    &   2  
        OR:     v   3
        IMPL:   >   4
        BICON:  <>  5
        UNI:    A
        EXI:    E
        ABS:    #
    
    THE GRAMMAR:
        vyraz ::= all male "[" E "]" | exist male "[" E "]" | E
        E ::= I | I "<>" E
        I ::= D | D ">" I
        D ::= C | C "|" D
        C ::= N | N "&" C
        N ::= literal | "!" literal
        literal ::= "(" E ")" | slovo "(" male ")" | slovo "(" konst ")"
        velke ::= ”A” | ”B” | ... | ”Y ” | ”Z”
        male ::= ”h” | ”i” | ... | ”y” | ”z”
        konst ::= ”a” | ”b” | ... | ”f ” | ”g”
        libovolne ::= male | konst
        all ::= "∀" | "A"
        exist ::= "∃" | "E"
        slovo ::= velke, {libovolne}

### How to install
To install dependencies on Ubuntu 22.04 run:

```bash
sudo apt install npm python3 python3-pip
```

```bash
pip install "fastapi[all]"
pip install "uvicorn[standard]"
cd web/
npm install
```

### Run the API
```bash
python3 -m uvicorn api.api:app --reload --port=8000
```

### Run the web
```bash
cd web/
npm run serve
```