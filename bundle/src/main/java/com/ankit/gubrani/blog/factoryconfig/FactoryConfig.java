package com.ankit.gubrani.blog.factoryconfig;

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.ConfigurationPolicy;
import org.apache.felix.scr.annotations.Property;
import org.apache.sling.commons.osgi.PropertiesUtil;
import org.osgi.service.component.ComponentContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Dictionary;

@Component(label = "Factory configuration", immediate = true, enabled = true, metatype = true,
        description = "This is factory configuration which acts as a interface for allowing user to enter property values",
        policy = ConfigurationPolicy.REQUIRE, configurationFactory = true)
@Property(name = "dummy.prop", label = "Dummy property", description = "This is just dummy property", value = "Dummy Value")
public class FactoryConfig {

    private static final Logger LOGGER = LoggerFactory.getLogger(FactoryConfig.class);

    @Activate
    public void activate(ComponentContext componentContext) {
        Dictionary properties = componentContext.getProperties();
        String dummyProperty = PropertiesUtil.toString(properties.get("dummy.prop"), "");
        LOGGER.info("Read the dummy property value : " + dummyProperty);
    }
}
