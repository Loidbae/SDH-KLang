import {
  definePlugin,
  PanelSection,
  PanelSectionRow,
  ServerAPI,
  DropdownItem,
  staticClasses,
  DropdownOption,
} from "decky-frontend-lib";

import { VFC, useState, useEffect } from "react";
import { FaKeyboard } from "react-icons/fa";
import * as backend from "./backend"

const Content: VFC<{ server: ServerAPI }> = ({server}) => {
  backend.setServer(server);

  const [layoutOptions, setlayoutOptions] = useState<DropdownOption[]>([]);
  const [variantOptions, setvariantOptions] = useState<DropdownOption[]>([]);

  const [currentLayout, setcurrentLayout] = useState<DropdownOption[]>([]);
  const [currentVariant, setcurrentVariant] = useState<DropdownOption[]>([]);

  const [_, setDummyResult] = useState<boolean>(false); 
  

  function dummyFuncTest() {
    backend.resolvePromise(backend.dummyFunction(), setDummyResult);
  }

  useEffect(() => {
    dummyFuncTest();
  }, []);

  useEffect(() => {
    backend.resolvePromise(backend.getCurrentLayout(), setcurrentLayout);
    backend.resolvePromise(backend.getCurrentVariant(), setcurrentVariant);
    
    backend.resolvePromise(backend.getLayoutOptions(), setlayoutOptions);
    backend.resolvePromise(backend.getVariantOptions(), setvariantOptions);

  },[])

  useEffect(() => {

    let layout_options = layoutOptions.map((layout) => {
      return{
        label:layout['label'],
        data:layout['data']
      }
    });

    setlayoutOptions(layout_options);
    
    let variant_options = variantOptions.map((variant) => {
      return{
        label:variant['label'],
        data:variant['data']
      }
    });
    
    setvariantOptions(variant_options);
  }, []);

  return (
    <PanelSection title="Settings">
      <p>For any changes to take effect, please switch to desktop mode and back OR reboot your steam deck</p>
      <PanelSectionRow>
        <DropdownItem
          rgOptions={layoutOptions}
          label="Layout"
          menuLabel="Select a Layout"
          selectedOption={currentLayout}
          onChange={(data) =>{
            backend.setLayout(data)
            backend.unsetVariant()
          }}
        />
      </PanelSectionRow>
      
      <PanelSectionRow>
        <DropdownItem
          rgOptions={variantOptions}
          label="Variant"
          menuLabel="Select a Variant"
          selectedOption={currentVariant}
          onChange={(data) => {
            backend.setVariant(data)
          }}
        />
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin((serverApi: ServerAPI ) => {
  return {
    title: <div className={staticClasses.Title}>KLang!</div>,
    content: <Content server={serverApi} />,
    icon: <FaKeyboard />,
    onDismount() {
    },
  };
});
