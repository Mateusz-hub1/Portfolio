const TIMER_LIMIT = 25 * 60;      // 25 minut
let categories = {}, currentCat, questions = [], idx = 0;
let answers = [], timer, streak = 0, bestStreak = 0, timeLeft = TIMER_LIMIT;

const selCat = q('#categorySelect'),
      card  = q('#quizCard'),
      qTxt  = q('#questionText'),
      aBox  = q('#answers'),
      timerEl=q('#timer'),
      prog  = q('#progress'),
      prevB = q('#prevBtn'),
      nextB = q('#nextBtn'),
      finB  = q('#finishBtn'),
      resultM=q('#resultModal'),
      scoreL = q('#scoreLine');

init();

async function init(){
  // wczytaj wszystkie jsony z katalogu data/
  for(const file of ['prawo_jazdy','egzamin_it','historia_pl']){
    const data = await fetch(`data/${file}.json`).then(r=>r.json());
    categories[data.id]=data;
    selCat.append(new Option(data.title,data.id));
  }
  selCat.onchange=startQuiz;
}

function startQuiz(){
  currentCat = categories[selCat.value];
  questions  = shuffle([...currentCat.questions]);
  answers    = Array(questions.length).fill(null);
  idx=0;streak=0;bestStreak=0;timeLeft=TIMER_LIMIT;
  renderQuestion();card.classList.remove('hidden');
  timer && clearInterval(timer);
  timer = setInterval(()=>{updateTimer()},1000);
}

function renderQuestion(){
  const qObj=questions[idx];
  qTxt.textContent=qObj.q;
  // media
  const mBox=q('#mediaBox');
  mBox.innerHTML='';
  if(qObj.media){
    if(qObj.media.type==='img'){
     const img = new Image();
      img.src = qObj.media.src;
      img.alt = '';
      img.classList.add('question-image'); // TO DODAJ
      mBox.append(img);
    }else if(qObj.media.type==='video'){
      const v=document.createElement('video');
      v.src=qObj.media.src;v.controls=true;v.width=480;mBox.append(v);
    }
  }
  // odpowiedzi
  aBox.innerHTML='';
  ['A','B','C','D'].forEach(key=>{
    const li=document.createElement('li');
    li.dataset.key=key;
    li.textContent=`${key}. ${qObj[key]}`;
    if(answers[idx]!==null){
      li.classList.add(answers[idx]===key ? (key===qObj.correct?'correct':'wrong') : '');
      if(key===qObj.correct && answers[idx]!==key) li.classList.add('correct');
    }
    li.onclick=()=>choose(key);
    aBox.append(li);
  });
  // nawigacja
  prevB.disabled = idx===0;
  nextB.disabled = idx===questions.length-1;
  finB.classList.toggle('hidden',idx!==questions.length-1);
  prog.style.width = `${(idx+1)/questions.length*100}%`;
}

function choose(k){
  const correct = questions[idx].correct;
  answers[idx]=k;
  if(k===correct){streak++;bestStreak=Math.max(bestStreak,streak);}
  else streak=0;
  renderQuestion();
}

prevB.onclick=()=>{if(idx>0){idx--;renderQuestion();}};
nextB.onclick=()=>{if(idx<questions.length-1){idx++;renderQuestion();}};
finB.onclick=endQuiz;

function endQuiz(){
  clearInterval(timer);
  const points = answers.reduce((s,a,i)=>s+(a===questions[i].correct),0);
  const spent  = TIMER_LIMIT-timeLeft;
  saveScore(points,spent,bestStreak);
  scoreL.textContent=`${points} / ${questions.length} poprawnych ❘ czas: ${fmt(spent)} ❘ najdłuższa seria: ${bestStreak}`;
  resultM.classList.remove('hidden');
}

function saveScore(p,t,st){
  const name = prompt('Podaj swoje imię:','Anon');
  if(!name) return;
  const rec = {name,points:p,time:t,streak:st,date:Date.now()};
  const key=`board_${currentCat.id}`;
  const board = JSON.parse(localStorage.getItem(key)||'[]');
  board.push(rec);
  localStorage.setItem(key,JSON.stringify(board));
}

function updateTimer(){
  timeLeft--; timerEl.textContent=fmt(timeLeft);
  if(timeLeft<=0){alert('Koniec czasu!');endQuiz();}
}

function fmt(sec){
  const m=String(Math.floor(sec/60)).padStart(2,'0'),
        s=String(sec%60).padStart(2,'0');
  return `${m}:${s}`;
}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function q(sel,par=document){return par.querySelector(sel);}
