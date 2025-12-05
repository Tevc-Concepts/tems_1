import{C as t,a as d}from"./circle-x-RwOzPd3h.js";import{c as a}from"./createLucideIcon-TnRFscOj.js";import{k as o,c as g,o as r,p as y,d as m,g as u,G as p,t as k,n as C}from"./vue-vendor-85nDNI24.js";/**
 * @license lucide-vue-next v0.545.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const b=a("circle-alert",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["line",{x1:"12",x2:"12",y1:"8",y2:"12",key:"1pkeuh"}],["line",{x1:"12",x2:"12.01",y1:"16",y2:"16",key:"4dfq90"}]]);/**
 * @license lucide-vue-next v0.545.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const f=a("circle-play",[["path",{d:"M9 9.003a1 1 0 0 1 1.517-.859l4.997 2.997a1 1 0 0 1 0 1.718l-4.997 2.997A1 1 0 0 1 9 14.996z",key:"kmsa83"}],["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}]]);/**
 * @license lucide-vue-next v0.545.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const e=a("clock",[["path",{d:"M12 6v6l4 2",key:"mmk7yg"}],["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}]]),A={__name:"StatusBadge",props:{status:{type:String,required:!0},label:{type:String,default:""}},setup(c){const s=c,l={Active:{class:"badge-success",icon:f},Completed:{class:"badge-success",icon:t},Assigned:{class:"badge-info",icon:e},Planned:{class:"badge-info",icon:e},Cancelled:{class:"badge-danger",icon:d},Open:{class:"badge-warning",icon:b},"In Progress":{class:"badge-warning",icon:e},Closed:{class:"badge-success",icon:t}},i=o(()=>l[s.status]?.class||"badge-info"),n=o(()=>l[s.status]?.icon||null);return(x,h)=>(r(),g("span",{class:C(["badge",i.value])},[n.value?(r(),y(p(n.value),{key:0,class:"w-3 h-3 mr-1"})):m("",!0),u(" "+k(c.label),1)],2))}};export{b as C,A as _,e as a};
//# sourceMappingURL=StatusBadge-q7HUT-w6.js.map
