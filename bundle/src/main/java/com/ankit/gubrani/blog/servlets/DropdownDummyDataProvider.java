package com.ankit.gubrani.blog.servlets;

import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Service;
import org.apache.felix.scr.annotations.sling.SlingServlet;
import org.apache.sling.api.SlingHttpServletRequest;
import org.apache.sling.api.SlingHttpServletResponse;
import org.apache.sling.api.servlets.SlingSafeMethodsServlet;
import org.apache.sling.commons.json.JSONException;
import org.apache.sling.commons.json.io.JSONWriter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

@Service(DropdownDummyDataProvider.class)
@SlingServlet(paths = {"/bin/codebrains"}, generateComponent = false)
@Component(label = "Dropdown Data data provider", description = "This servlet provides dummy data for the custom drop down",
        enabled = true, immediate = true, metatype = false)
public class DropdownDummyDataProvider extends SlingSafeMethodsServlet {

    private static final Logger LOGGER = LoggerFactory.getLogger(DropdownDummyDataProvider.class);

    @Override
    protected void doGet(SlingHttpServletRequest request, SlingHttpServletResponse response) {
        try {
            JSONWriter jsonWriter = new JSONWriter(response.getWriter());
            jsonWriter.array();

            //This loop creates multiple objects under a array that will be returned.
            for (int i = 0; i < 5; i++) {
                jsonWriter.object().key("text").value("CodeBrains_Text_" + i).key("value").value("CodeBrains_Value_" + i);
                jsonWriter.endObject();
            }

            jsonWriter.endArray();
        } catch (JSONException e) {
            LOGGER.error("Json Exception occured while adding data to JSON Object : ", e);
        } catch (IOException e) {
            LOGGER.error("IOException occured while getting Print Writer from SlingServletResponse : ", e);
        }
    }
}
