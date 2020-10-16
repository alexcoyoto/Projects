package com.example.myrssreader.AsyncTasks;

import android.os.AsyncTask;
import android.widget.Toast;

import com.example.myrssreader.MainActivity;
import com.example.myrssreader.Models.RSSModel;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;


public class ParsingAsync extends AsyncTask<String, Void, ArrayList<RSSModel>> {
    private MainActivity activity;
    private String str;

    public ParsingAsync(MainActivity activity)
    {
        this.activity = activity;
    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();

    }

    @Override
    protected ArrayList<RSSModel> doInBackground(String... urls) {
        try {
            str = urls[0];
            return getRSSItems(urls[0]);
        }
        catch (Exception ex)
        {
            Toast.makeText(activity, "Адбылася памылка", Toast.LENGTH_SHORT).show();
            ex.printStackTrace();
        }
        return null;
    }

    private ArrayList<RSSModel> getRSSItems(String url)throws SAXException, IOException, ParserConfigurationException
    {
        ArrayList<RSSModel> items = new ArrayList<>();
        String title = "", link = "", description = "";
        String currentTag = "";

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance(); // получить анализатор для создания dom объектов
        DocumentBuilder documentBuilder = factory.newDocumentBuilder(); // document from xml
        Document document = documentBuilder.parse(url);
        document.getDocumentElement().normalize();
        NodeList itemList = document.getElementsByTagName("item");
        for (int i = 0; i < itemList.getLength(); i++) {
            String URL = "", extraURL = "";
            if (i > 9)
                break;
            Element item = (Element) itemList.item(i);
            NodeList list = item.getElementsByTagName("link");
            if (list.getLength() > 0) {
                Element linkElement = (Element) list.item(0);
                link = linkElement.getTextContent();
            }

            list = item.getElementsByTagName("title");
            if (list.getLength() > 0) {
                Element titleElement = (Element) list.item(0);
                title = titleElement.getTextContent();
            } else
                title = "";

            list = item.getElementsByTagName("description");
            if (list.getLength() > 0) {
                Element descriptionElement = (Element) list.item(0);
                description = descriptionElement.getTextContent();




                Pattern p = Pattern.compile("src=\".+?\"");
                Matcher m = p.matcher(description);
                if (m.find()) {
                    String str = m.group();
                    extraURL = str.substring(5, str.length() - 1); // 5 - http... str - 1 = .."
                }


                Pattern pattern = Pattern.compile("<.+?>"); // delete all tags
                Matcher matcher = pattern.matcher(description);
                String newStr = matcher.replaceAll("");
                description = newStr;
            } else
                description = "";


            list = item.getElementsByTagName("enclosure");
            if (list.getLength() > 0) {
                Element enclosureElement = (Element) list.item(0);
                String type = enclosureElement.getAttribute("type");
                if (type.equals("image/jpeg") || type.equals("image/png")) {
                    URL = enclosureElement.getAttribute("url");
                    items.add(new RSSModel(title, currentTag, description, link, URL));
                } else {
                    if (extraURL.equals("")) {
                        items.add(new RSSModel(title, currentTag, description, link, ""));
                    } else
                        items.add(new RSSModel(title, currentTag, description, link, extraURL));
                }
            } else {
                if (extraURL.equals("")) {
                    items.add(new RSSModel(title, currentTag, description, link, ""));
                } else
                    items.add(new RSSModel(title, currentTag, description, link, extraURL));
            }
        }
        return items;
    }

    @Override
    protected void onPostExecute(ArrayList<RSSModel> result) {
        super.onPostExecute(result);
        if (result != null)
        {
            activity.onLoadFinished(result);
            activity.saveToDatabase(result, str);
        }
        else{
            Toast.makeText(activity, "Няма вынікаў", Toast.LENGTH_LONG).show();
        }
    }

}
