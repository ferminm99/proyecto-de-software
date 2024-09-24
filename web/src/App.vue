<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light py-0 topnav">
      <router-link to="/" class="navbar-brand">SalvAR</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <!--  <a class="nav-link" href="#"
              >Home <span class="sr-only">(current)</span></a
            >-->
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/puntosDeEncuentros" class="nav-link">Puntos y Recorridos</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/zonasInundables" class="nav-link">Zonas Inundables</router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              id="navbarDropdownMenuLink"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              style="cursor:pointer">
              Denuncia
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <router-link to="/crearDenuncia" class="dropdown-item">Crear Denuncia</router-link>
              <router-link to="/verDenuncia" class="dropdown-item">Ver Denuncia</router-link>
            </div>
          </li>
          <li class="nav-item">
            <router-link to="/estadisticas" class="nav-link">Estadisticas</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <!-- Aca se muestra la vista de la ruta elegida -->
    <router-view />
    <!--Fin-->
  </div>
</template>

<style src="./assets/styles.css"></style>


