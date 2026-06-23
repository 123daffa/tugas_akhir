<template>
  <section id="landing">
    <div class="home">
    <ul class="home-features">
      <li class="home-feature-list">Pemeriksa Fakta berbahasa Indonesia, bertenaga AI</li>
    </ul>
    <h1 class="home-title">Periksa Kebenaran</h1>
    <h1 class="home-subtitle">dengan tenang.</h1>
    <p class="home-paragraf">Tempelkan klaim, kutipan berita, atau pesan berantai. Kami bantu telusuri konteks, sebutkan ketidakpastian, 
      dan ajak Anda berpikir jernih.</p>
      <div class="btn-group">
          <RouterLink to="/deteksi" class="btn-mulai">Mulai Periksa Klaim</RouterLink>
          <RouterLink to="/tentang" class="btn-tentang">Bagaimana cara kerjanya?</RouterLink>
      </div>
      <div class="home-claim">
        <ul class="home-claim-list">
          <li class="home-claim-fakta">Fakta</li>
          <li class="home-claim-false">False Content</li>
          <li class="home-claim-misleading">Misleading Content</li>
          <li class="home-claim-fabricated">Fabricated Content</li>
        </ul>
      </div>  
    </div>
  </section>

  <section id="service">
    <div></div>
  </section>
</template>

<style scoped>
section {
  padding: 64px 128px;
}

.home {
  text-align: center;
}

#landing {
  align-items: center;
  margin-top: 30px;
}
.home-features {
  list-style-type: none;
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.home-feature-list {
  width: fit-content;
  background-color: white;
  border: 2px solid #808080;
  color: black;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
}
h1 {
  margin: 0;
  line-height: 1.2;
  padding-bottom: 5px;
}
.home-title {
  font-weight: bold;
  font-size: 65px;
  color: black;
}
.home-subtitle {
  font-weight: bold;
  font-size: 65px;
  background: linear-gradient(
      90deg,
      #4f6677 0%,
      #2f8f8b 45%,
      #20d48a 100%
    );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  }
.home-paragraf { 
  max-width: 900px;
  font-size: 18px;
  line-height: 1.4;
  text-align: center;
  margin: 30px auto 0;
  padding: 5px 100px;
}

.btn-group {
  margin-top: 30px;
  font-size: 20px;
  margin-bottom: 80px;
}

.btn-mulai {
  margin-right: 50px;
  background-color: #1B2B4B;
  padding: 10px 35px;
  border: 2px solid ;
  color: white;
  border-radius: 10px;
}

.btn-tentang {
  background-color: white;
  padding: 10px 30px;
  border: 2px solid #808080;
  color: black;
  border-radius: 10px;
}

.home-claim-list {
  margin-top: 60px;
  list-style-type: none;
  display: flex;
  justify-content: center;
  gap: 40px;
}

.home-claim-fakta {
  background-color: #20d48a;
  color: white;
  padding: 10px 25px;
  border-radius: 20px;
}
.home-claim-false {
  background-color: #ff4d4d;
  color: white;
  padding: 10px 25px;
  border-radius: 20px;
}
.home-claim-misleading {
  background-color: #ffcc00;
  color: white;
  padding: 10px 25px;
  border-radius: 20px;
}
.home-claim-fabricated {
  background-color: #808080;
  color: white;
  padding: 10px 25px;
  border-radius: 20px;
}
</style>