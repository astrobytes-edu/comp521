export default {
  render({el,model}) {
    const frame=document.createElement('iframe');
    frame.src=model.get('figureUrl');
    frame.title='Kepler geometry: synchronized clock, construction, and physical direction';
    frame.loading='lazy';
    frame.style.cssText='display:block;width:100%;height:870px;border:0;border-radius:16px;background:#0b1220;';
    const size=event=>{
      if(event.source!==frame.contentWindow || event.origin!==location.origin ||
         event.data?.type!=='comp521-kepler-size') return;
      const height=Number(event.data.height);
      if(Number.isFinite(height) && height>=300 && height<=2200) frame.style.height=height+'px';
    };
    const pause=()=>frame.contentWindow?.postMessage({type:'comp521-kepler-pause'},location.origin);
    const visibility=()=>{if(document.hidden)pause();};
    const observer=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)pause();});
    observer.observe(frame);
    window.addEventListener('message',size);
    document.addEventListener('visibilitychange',visibility);
    el.replaceChildren(frame);
    return ()=>{pause();observer.disconnect();window.removeEventListener('message',size);
      document.removeEventListener('visibilitychange',visibility);frame.remove();};
  },
};
