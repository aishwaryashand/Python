package main

import (
	// "os"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"github.com/gin-gonic/gin"
	"encoding/json"
)

type Details struct{
	took int
	timed_out bool
	_shards []Shards
	hits []Hits
}

type Shards struct{
	total int
	successful int
	skipped int
	failed int
}

type Hits struct{
	total []Total
	max_score int
	hits []Hits2
}

type Total struct{
	value int
	relation string
}

type Hits2 struct{
	_index string
	_type string
	_id string
	_score int
	_source []Source
}

type Source struct{
	id int
	version string
	email string
	lastname string
	timestamp string
	firstname string
	regdate string
}

func script(c *gin.Context) {
	lname := c.Query("lname")
	client := &http.Client{}
	var a = "https://testing-998905.es.eastus2.azure.elastic-cloud.com:9243/demo_index/_search?q=lastname:"+lname
	fmt.Println(a)
	req, err := http.NewRequest("GET", "https://testing-998905.es.eastus2.azure.elastic-cloud.com:9243/demo_index/_search?q=lastname:"+lname, nil)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
	req.Header.Set("Accept-Language", "en-US,en;q=0.5")
	req.Header.Set("Authorization", "Basic ZWxhc3RpYzpKN2htbllMcmZPajlLNmNWMUJiTmJQeHI=")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Upgrade-Insecure-Requests", "1")
	req.Header.Set("Cache-Control", "max-age=0")
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	bodyText, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	// fmt.Printf("%s\n", bodyText)

	var data Details
	// var responses []interface{}
	// // var response map[string]string
	// response := make(map[string]string)
	// response["took"]
	err1 := json.Unmarshal(bodyText, &data)
	if err1 != nil {
		log.Fatal(err1)
	}
	fmt.Println("Results: %v\n", data)
	// os.Exit(0)


	c.JSON(200, bodyText)
}


func main() {
	r := gin.Default()
	r.GET("/",script)
	r.Run()
}

