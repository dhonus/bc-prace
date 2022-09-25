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
        S -> Q[E]
        Q -> ∀V | ∃V
        E -> B
        B -> I | I <> B
        I -> D | D > I
        D -> C | C '|' D
        C -> N | N & C
        N -> F | !F
        F = W(V)
        V -> [a..z]
        V' -> VV' | eps
        W -> [A..Z] V'

* 4 predikáty limit
* hloubka stromu cca 3
* uzavřené formule
* bez funkcí, jedna proměnná
* kvantifikátory kalkulačka/kbd input
* převod do int formy; gramatika na validaci vstupu
* export zadání do txt
* export výsledku do pdf
* výsl. diagram libovolně; pref klas. venn
* rozkliknutelné články ve výsl. diagramu + odůvodnění
* při chybě zápisu vypsat důvod
* odkrokovat vč. změny diagramu při každém kroku
* řešení z obou stran ( uživatel zadá výsledek -> kontrola )
* zadání na elogice, přepnout si ročník 
* **do konce listopadu!**
* ~26. zář. další konzultace


npm install -g @vue/cli
pip install "fastapi[all]" # test removing all at the end
pip install "uvicorn[standard]"
npm install axios
npm install --save-dev node-sass sass-loader