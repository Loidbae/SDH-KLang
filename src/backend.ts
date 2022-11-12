import {DropdownOption, ServerAPI } from "decky-frontend-lib"

var server: ServerAPI | undefined = undefined;

export function resolvePromise(promise: Promise<any>, callback: any) {
    (async function () {
        let data = await promise;
        if (data.success)
            callback(data.result);
    })();
}

export function callBackendFunction(promise: Promise<any>) {
    (async function () {
        await promise;
    })();
}

export function setServer(s: ServerAPI) {
    server = s;
}

export function dummyFunction(): Promise<any> {
    return server!.callPluginMethod("dummy_function", {});
}

export function setVariant(selectedVariant: DropdownOption){
    return server!.callPluginMethod("set_kb_variant", {"variant" : selectedVariant.data as string});
}

export function setLayout(selectedLayout: DropdownOption){
    return server!.callPluginMethod("set_kb_layout", {"layout": selectedLayout.data as string});
}

export function getVariantOptions(){
    return server!.callPluginMethod("get_kb_variants",{});
}

export function getLayoutOptions(){
    return server!.callPluginMethod("get_kb_layouts", {});
}

export function getCurrentVariant(){
    return server!.callPluginMethod("get_current_kb_variant", {});
}

export function getCurrentLayout(){
    return server!.callPluginMethod("get_current_kb_layout", {});
}

export function unsetVariant() {
    return server!.callPluginMethod("unset_variant", {});
}