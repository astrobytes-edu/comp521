// Course lecture MyST directives. Asset links remain ordinary, downloadable references.
const directory = new URL('.', import.meta.url).pathname;
function relative(from, target) {
  const a=from.split('/').filter(Boolean), b=target.split('/').filter(Boolean);
  let i=0; while(i<a.length && a[i]===b[i]) i++;
  return [...a.slice(i).map(()=> '..'), ...b.slice(i)].join('/');
}
function widget(vfile, file, model, id) {
  return {type:'anywidget',esm:relative(vfile.path.replace(/\/[^/]*$/,''),directory+file),model,id};
}
export default {
  name:'Lecture presentation and films',
  directives:[{
    name:'lecture-controls', body:{type:String,required:false},
    options:{id:{type:String,required:true}},
    run(data,vfile) { return [widget(vfile,'lecture-controls.mjs',{},data.options.id)]; },
  },{
    name:'lecture-film', body:{type:String,required:true},
    options:{video:{type:String,required:true},poster:{type:String,required:true},id:{type:String,required:true}},
    run(data,vfile) {
      const {video,poster,id}=data.options;
      return [{type:'div',class:'lecture-film',children:[
        {type:'paragraph',children:[{type:'image',url:poster,alt:data.body.trim()}]},
        {type:'paragraph',children:[{type:'link',url:video,children:[{type:'text',value:'Open or download this short animation'}]}]},
        widget(vfile,'lecture-player.mjs',{description:data.body.trim(),mediaUrl:`${(process.env.BASE_URL || '').replace(/\/$/,'')}/media/${video.split('/').pop()}`},id),
      ]}];
    },
  }],
};
