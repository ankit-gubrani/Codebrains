package com.ankit.gubrani.blog.factoryconfig;

import org.apache.felix.scr.annotations.*;

import java.util.ArrayList;
import java.util.List;

@Component(label = "Factory Congifuration", description = "", immediate = true, metatype = true, enabled = true)
@Service(FactoryConfigConsumer.class)
public class FactoryConfigConsumer {

    @Reference(referenceInterface = FactoryConfig.class, cardinality = ReferenceCardinality.OPTIONAL_MULTIPLE,
            policy = ReferencePolicy.DYNAMIC, name = "Code Brains Demo Factory configurations")
    private List<FactoryConfig> factoryConfigs;

    protected synchronized void bindFactoryConfig(final FactoryConfig config) {
        if (factoryConfigs == null) {
            factoryConfigs = new ArrayList<FactoryConfig>();
        }

        factoryConfigs.add(config);
    }

    protected synchronized void unbindFactoryConfig(final FactoryConfig config) {
        factoryConfigs.remove(config);
    }
}
