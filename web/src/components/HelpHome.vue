<template>
  <div class="help">
    <div class="help-body">
      <button class="closeButton" @click="$emit('close')">X</button>
      <h2>Nápověda</h2>
      <h3>Zadání premis</h3>
      <ol>
        <li>Do vstupních polí zadejte premisy úsudku. Syntaxe je popsána na pravé straně nástroje.</li>
        <li>Pro přidání další premisy klikněte na tlačítko &bdquo;<b>+</b>".</li>
        <li>Pro vyhodnocení úsudku klikněte na tlačítko &bdquo;<b>Vyhodnotit</b>", nebo použijte klávesovou zkratku CTRL + ENTER</li>
      </ol>
      <h3>Vymezení jazyka</h3>
      <ul>
        <li> Formule musí být uzavřené. </li>
        <li> Ve formuli se musí vyskytovat právě jedna proměnná, nebo konstanta.</li>
        <li> Podporovány jsou pouze unární predikátové symboly.</li>
        <li> Predikátové symboly mohou být nahrazeny celými slovy. Musí začínat velkým písmenem. Validní jsou např. „C“, „Člověk“.</li>
        <li> Logické spojky lze ve vstupním řetězci nahradit alternativními symboly</li>
        <li> Funkční symboly nejsou podporovány (pouze symboly konstant).</li>
        <li> Lze používat hranaté a jednoduché závorky.</li>
      </ul>
      <p>K dispozici je virtuální klávesnice logických spojek. Lze také využít alternativních znaků popsaných v tabulce.</p>

      <h3>Označení oblastí</h3>
        <p>Pro jednoduchost jsou oblasti ve výstupu označovány následovně:</p>
        <ul>
            <li>Universum je označeno znakem „Ω“</li>
            <li>„A“ reprezentuje množinu prvků, které náleží A' a žádné jiné množině</li>
            <li>„A ∩ B“ označuje oblast, která náleží A' i B'</li>
        </ul>

      <h3>Příklad zadání</h3>
      <img src="../assets/help_home.gif" alt="Nápověda" />
      <h3>Výstup</h3>
      <p>Program vypíše informaci o pravdivosti, výsledný diagram a odůvodnění.</p>
      <p>Lze zobrazit kroky, které vedly k výsledku pomocí &bdquo;<b>Odkrokovat</b>"</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelpHome"
}
</script>

<style scoped>
  .help {
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 100;
    overflow: hidden;
  }
  .help-body {
    margin: 1rem auto;
    padding: 1rem;
    background-color: white;
    border-radius: 0.5rem;
    width: 50%;
    height: fit-content;
    overflow: auto;
    text-align: left;
  }
  @media screen and (max-width: 1300px) {
    .help-body {
      width: 60%;
    }
  }
  @media screen and (max-width: 1000px) {
    .help-body {
      width: 90%;
      height: 90%;
    }
  }
  h2 {
    margin: .3rem 0 1rem 0;
    text-align: center;
  }
  h3 {
    margin: 1.5rem 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 500;
    line-height: 1.5;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  ol{
    list-style-type: decimal;
    padding-left: 1.5rem;
    margin-top: 0;
    line-height: 2;
  }
  ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-top: 0;
    line-height: 2;
  }
  li {
    margin-bottom: 0.5rem;
    text-align: left;
  }
  img {
    width: 80%;
    margin: 0 auto;
    display: block;
    border-radius: 7px;
    border: 1px solid #ddd;
  }
  .closeButton {
    float: right;
    border: none;
    background-color: whitesmoke;
    border-radius: 50%;
    border: 1px solid #ab94c4;
    font-size: 1rem;
    width: 1.7rem;
    height: 1.7rem;
    cursor: pointer;
  }
  .closeButton:hover {
    background-color: #ab94c4;
    color: white;
  }
</style>