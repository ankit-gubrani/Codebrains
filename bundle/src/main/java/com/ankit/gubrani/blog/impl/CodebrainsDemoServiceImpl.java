package com.ankit.gubrani.blog.impl;

import com.ankit.gubrani.blog.CodebrainsDemoService;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Property;
import org.apache.felix.scr.annotations.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service(CodebrainsDemoService.class)
@Component(enabled = true, immediate = true, metatype = false)
@Property(label = "author.name", name = "author", value = "ankit.gubrani",
        description = "This property stores name of the author of codebrains blog")
public class CodebrainsDemoServiceImpl implements CodebrainsDemoService {

    private static final Logger LOGGER = LoggerFactory.getLogger(CodebrainsDemoServiceImpl.class);

    @Override
    public void showBlog() {
        System.out.println("Hello World welcome to Codebrains.com");
    }
}
