<template>
  <div class="w-100">
    <div id="cartelInicial">
      <h1>Bienvenido a SalvAR</h1>
    </div>
    <div id="carrousel" class="carousel slide" data-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img
            src="../assets/img/meridianov.jpg"
            class="d-block w-100"
            alt="no carga"
          />
        </div>
        <div class="carousel-item">
          <img
            src="../assets/img/Estadio.jpg"
            class="d-block w-100"
            alt="no carga"
          />
        </div>
        <div class="carousel-item">
          <img
            src="../assets/img/hipodromo.jpg"
            class="d-block w-100"
            alt="no carga"
          />
        </div>
        <div class="carousel-item">
          <img
            src="../assets/img/dardoRocha.jpg"
            class="d-block w-100"
            alt="no carga"
          />
        </div>
        <div class="carousel-item">
          <img
            src="../assets/img/polideportivo.jpg"
            class="d-block w-100"
            alt="no carga"
          />
        </div>
      </div>
    </div>
    <img src="../assets/img/fotointemedia.jpg" alt="no carga" class="w-100">

    <!-- Fin carrousel -->
    <div class="container">
    <div class="row mx-0">
      <CardInfo title="Puntos de Encuentro" description="Aqui podra ver los puntos de encuentro ante una emergencia" link="puntosDeEncuentros" img="punto_de_encuentro.jpg" />
      <CardInfo title="Recorrido de Evacuacion" description="Mira el recorrido de evacuacion más cercano a tu ubicación" link="puntosDeEncuentros" img="ruta-evacuacion.jpg" />
      <CardInfo title="Zonas Inundables" description="Seccion que muestra las zonas mas propensas a inundarse" link="zonasInundables" img="zonas_inundables.png" />
      <CardInfo title="Haz tu Denuncia" description="Aqui podras hacer un denuncia respecto al estado de las calles, etc." link="crearDenuncia" img="denuncia.jpg" />
      <CardInfo title="Mostrar las Denuncias" description="Mira las denuncias que han sido confirmadas y sus detalles" link="verDenuncia" img="denuncia_confirmadas.jpg" />
      <CardInfo title="Estadisticas" description="Observa las estadisticas que se fueron recolectado" link="estadisticas" img="estadisticas.jpg" />
    </div>
    </div>
  </div>
</template>
<script>
import CardInfo from './CardInfo'
export default {
  name: "Home",
  components: {
    CardInfo
  },
  data: () => ({}),
};
</script>