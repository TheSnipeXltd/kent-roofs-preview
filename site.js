const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const root=document.documentElement,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;

/* opening animation (home page only): plays on first visit and on refresh; click or Esc skips */
const intro=$('#intro');const navT=(performance.getEntriesByType('navigation')[0]||{}).type;
let internal=false;try{const r=new URL(document.referrer),norm=x=>x.replace(/index\.html$/,'').replace(/\/$/,'');internal=r.origin===location.origin&&norm(r.pathname)!==norm(location.pathname)}catch(e){} // refreshing the same page replays it; arriving from another page of the site skips it
const seen=navT!=='reload'&&(internal||navT==='back_forward');
function endIntro(){
  if(!intro||intro.dataset.done)return;intro.dataset.done=1;
  root.classList.remove('lock');root.classList.add('ready');intro.style.pointerEvents='none';intro.classList.add('out');
  setTimeout(()=>intro.remove(),1000);
}
if(!intro||reduce||seen){intro&&intro.remove();root.classList.add('ready')}
else{root.classList.add('lock');setTimeout(endIntro,2600);intro.addEventListener('click',endIntro);addEventListener('keydown',e=>{if(e.key==='Escape')endIntro()})}

/* header: progress bar and solid background; scroll work is batched into one frame */
const hdr=$('#hdr'),prog=$('#prog'),nav=$('#nav'),burger=$('#burger');
let maxScroll=1,solid=false,ticking=false;
const measure=()=>{maxScroll=Math.max(1,document.documentElement.scrollHeight-innerHeight)};
function paint(){ticking=false;const y=scrollY;prog.style.setProperty('--p',Math.min(1,y/maxScroll));const s=y>40;if(s!==solid){solid=s;hdr.classList.toggle('solid',s)}}
addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(paint)}},{passive:true});
addEventListener('resize',()=>{measure();paint();if(innerWidth>900)closeMenu()});
if('ResizeObserver' in window)new ResizeObserver(()=>{measure();paint()}).observe(document.body);
measure();paint();

/* menu: staggered slide-in; closes on a tap outside, a link, Esc, or a resize to desktop */
const scrim=document.createElement('div');scrim.className='scrim';document.body.appendChild(scrim);
$$('#nav a').forEach((a,i)=>a.style.setProperty('--i',i));
function setMenu(open){nav.classList.toggle('open',open);scrim.classList.toggle('on',open);root.classList.toggle('menu-open',open);burger.setAttribute('aria-expanded',open);burger.setAttribute('aria-label',open?'Close menu':'Menu')}
function closeMenu(){if(nav.classList.contains('open'))setMenu(false)}
burger.addEventListener('click',()=>setMenu(!nav.classList.contains('open')));
scrim.addEventListener('click',closeMenu);
$$('#nav a').forEach(a=>a.addEventListener('click',closeMenu));
addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});

/* press feedback: a ripple from the exact point of the tap (buttons never move away from the cursor) */
if(!reduce)document.addEventListener('pointerdown',e=>{
  const t=e.target.closest('.btn,.chip,.round,.callfab,.chat');if(!t)return;
  const r=t.getBoundingClientRect(),d=Math.max(r.width,r.height)*2.2,el=document.createElement('span');
  el.className='rip';el.style.cssText=`width:${d}px;height:${d}px;left:${e.clientX-r.left-d/2}px;top:${e.clientY-r.top-d/2}px`;
  t.appendChild(el);el.addEventListener('animationend',()=>el.remove());setTimeout(()=>el.remove(),900); // safety clean-up
},{passive:true});

/* hero photo parallax (mouse only, one update per frame) */
if(fine&&!reduce){const hero=$('#hero');if(hero){let px=0,py=0,raf=0;
  hero.addEventListener('pointermove',e=>{const r=hero.getBoundingClientRect();px=((e.clientX-r.left)/r.width-.5)*2;py=((e.clientY-r.top)/r.height-.5)*2;
    if(!raf)raf=requestAnimationFrame(()=>{raf=0;hero.style.setProperty('--px',px);hero.style.setProperty('--py',py)})},{passive:true})}}

/* services (home): hover or tap a service, its photo wipes in */
const items=$$('.svc-item'),imgs=$$('#stage img');
if(items.length&&imgs.length){
  let cur=0,z=1;
  const setSvc=i=>{
    items.forEach((it,k)=>{it.classList.toggle('on',k===i);$('button',it).setAttribute('aria-expanded',k===i)});
    if(i===cur&&imgs[i].dataset.shown)return;cur=i;const im=imgs[i];im.dataset.shown=1;
    if(reduce){im.style.zIndex=++z;return}
    im.style.transition='none';im.style.clipPath='inset(0 0 100% 0)';im.style.zIndex=++z;im.offsetWidth;
    im.style.transition='clip-path .85s cubic-bezier(.77,0,.18,1)';im.style.clipPath='inset(0)';
  };
  items.forEach((it,i)=>{
    const b=$('button',it);b.addEventListener('click',()=>setSvc(i));b.addEventListener('focus',()=>setSvc(i));
    it.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'&&matchMedia('(min-width:901px)').matches)setSvc(i)});
  });
  setSvc(0);
}

/* projects rail (home): drag, buttons, progress */
const rail=$('#rail');
if(rail){
  const rp=$('#rprog');
  const upd=()=>rp.parentElement.style.setProperty('--r',Math.min(1,(rail.scrollLeft+rail.clientWidth)/rail.scrollWidth));
  rail.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
  const step=()=>rail.querySelector('figure').offsetWidth+22;
  $('#prev').addEventListener('click',()=>rail.scrollBy({left:-step(),behavior:'smooth'}));
  $('#next').addEventListener('click',()=>rail.scrollBy({left:step(),behavior:'smooth'}));
  let down=false,sx=0,sl=0;
  rail.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;sx=e.clientX;sl=rail.scrollLeft;rail.classList.add('drag')});
  addEventListener('pointermove',e=>{if(down)rail.scrollLeft=sl-(e.clientX-sx)});
  addEventListener('pointerup',()=>{if(!down)return;down=false;rail.classList.remove('drag')});
  rail.addEventListener('keydown',e=>{if(e.key==='ArrowRight')$('#next').click();if(e.key==='ArrowLeft')$('#prev').click()});
}

/* quote form (home): builds a WhatsApp message */
const qf=$('#qf');
if(qf){
  const chips=$$('.chip'),err=$('#err'),sendT=$('#sendT');
  chips.forEach(c=>c.addEventListener('click',()=>{
    const on=c.getAttribute('aria-pressed')!=='true';c.setAttribute('aria-pressed',on);err.textContent='';
  }));
  qf.addEventListener('submit',e=>{
    e.preventDefault();
    const picked=chips.filter(c=>c.getAttribute('aria-pressed')==='true').map(c=>c.textContent);
    const pc=$('#pc').value.trim(),nm=$('#nm').value.trim(),dt=$('#dt').value.trim();
    if(!picked.length){err.textContent='Choose at least one service, or pick Not sure.';return}
    if(!/^[A-Za-z]{1,2}\d[A-Za-z\d]?\s*\d[A-Za-z]{2}$/.test(pc)){err.textContent='Enter a full UK postcode, for example ME14 1AB.';$('#pc').focus();return}
    err.textContent='';
    const msg=`Hi Kent Roofs, I'd like a quote.\nServices: ${picked.join(', ')}\nPostcode: ${pc.toUpperCase()}`+(nm?`\nName: ${nm}`:'')+(dt?`\nDetails: ${dt}`:'');
    sendT.textContent='Opening WhatsApp';
    window.open('https://wa.me/447961994386?text='+encodeURIComponent(msg),'_blank','noopener');
    setTimeout(()=>sendT.textContent='Send on WhatsApp',2500);
  });
}

/* FAQ (service pages): one open at a time */
const faqs=$$('.faq-item');
faqs.forEach(it=>$('button',it).addEventListener('click',()=>{
  const open=!it.classList.contains('on');
  faqs.forEach(o=>{o.classList.remove('on');$('button',o).setAttribute('aria-expanded','false')});
  if(open){it.classList.add('on');$('button',it).setAttribute('aria-expanded','true')}
}));

/* projects page: filter by service + lightbox */
const grid=$('#grid');
if(grid){
  const tiles=$$('.tile',grid),fchips=$$('#filters .chip'),cnt=$('#count'),lb=$('#lb');
  let vis=tiles,idx=0,opener=null;
  const applyFilter=tag=>{
    fchips.forEach(c=>c.setAttribute('aria-pressed',c.dataset.f===tag));
    let k=0;
    tiles.forEach(t=>{
      const show=tag==='all'||t.dataset.tags.split(' ').includes(tag);
      t.classList.remove('pop');
      if(show){t.hidden=false;t.classList.remove('out');if(!reduce){t.style.setProperty('--k',k++);void t.offsetWidth;t.classList.add('pop')}}
      else{t.hidden=true}
    });
    vis=tiles.filter(t=>!t.hidden);cnt.textContent=`Showing ${vis.length} ${vis.length===1?'photo':'photos'}`;
  };
  fchips.forEach(c=>c.addEventListener('click',()=>applyFilter(c.dataset.f)));
  const show=i=>{
    idx=(i+vis.length)%vis.length;const t=vis[idx],im=$('img',t);
    $('#lbImg').src=im.src;$('#lbImg').alt=im.alt;$('#lbT').textContent=t.dataset.title;$('#lbN').textContent=`${idx+1} of ${vis.length}`;
    $('#lbQ').href='https://wa.me/447961994386?text='+encodeURIComponent(`Hi Kent Roofs, I saw your "${t.dataset.title}" photo and I'd like a quote for something similar.`);
  };
  const open=t=>{opener=t;show(vis.indexOf(t));lb.classList.add('open');lb.setAttribute('aria-hidden','false');root.classList.add('lock');$('#lbX').focus()};
  const close=()=>{lb.classList.remove('open');lb.setAttribute('aria-hidden','true');root.classList.remove('lock');opener&&opener.focus()};
  tiles.forEach(t=>t.addEventListener('click',()=>open(t)));
  $('#lbX').addEventListener('click',close);$('#lbP').addEventListener('click',()=>show(idx-1));$('#lbNx').addEventListener('click',()=>show(idx+1));
  lb.addEventListener('click',e=>{if(e.target===lb||e.target.tagName==='FIGURE')close()});
  addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;
    if(e.key==='Escape')close();if(e.key==='ArrowRight')show(idx+1);if(e.key==='ArrowLeft')show(idx-1);
    if(e.key==='Tab'){const f=[$('#lbP'),$('#lbNx'),$('#lbX'),$('#lbQ')],i=f.indexOf(document.activeElement);e.preventDefault();f[(i+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
  let tx=0;lb.addEventListener('touchstart',e=>{tx=e.changedTouches[0].clientX},{passive:true});
  lb.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)show(idx+(d<0?1:-1))});
  applyFilter('all');
}
