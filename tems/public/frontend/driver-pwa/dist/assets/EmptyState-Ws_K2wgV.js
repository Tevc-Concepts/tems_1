import{c}from"./createLucideIcon-TnRFscOj.js";import{c as n,o as e,a,d as l,p as r,G as m,t as o}from"./vue-vendor-85nDNI24.js";/**
 * @license lucide-vue-next v0.545.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const d=c("inbox",[["polyline",{points:"22 12 16 12 14 15 10 15 8 12 2 12",key:"o97t9d"}],["path",{d:"M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z",key:"oot6mr"}]]),y={class:"flex flex-col items-center justify-center py-12 px-4 text-center"},f={class:"w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4"},p={class:"text-lg font-semibold text-gray-900 mb-2"},u={class:"text-sm text-gray-600 mb-6 max-w-sm"},h={__name:"EmptyState",props:{icon:{type:Object,default:()=>d},title:{type:String,default:"No items found"},message:{type:String,default:"There are no items to display at the moment."},actionLabel:{type:String,default:""}},emits:["action"],setup(t){return(i,s)=>(e(),n("div",y,[a("div",f,[(e(),r(m(t.icon),{class:"w-10 h-10 text-gray-400"}))]),a("h3",p,o(t.title),1),a("p",u,o(t.message),1),t.actionLabel?(e(),n("button",{key:0,onClick:s[0]||(s[0]=x=>i.$emit("action")),class:"btn-primary"},o(t.actionLabel),1)):l("",!0)]))}};export{h as _};
//# sourceMappingURL=EmptyState-Ws_K2wgV.js.map
