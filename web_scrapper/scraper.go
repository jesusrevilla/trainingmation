package main

import (
	"context"
	"log"
	"os"
	"strings"

	"github.com/chromedp/chromedp"
)

func main() {

	logger := log.New(os.Stdout, "INFO: ", log.Ldate|log.Ltime)

	// initialize a controllable Chrome instance
	ctx, cancel := chromedp.NewContext(
		context.Background(),
	)
	// to release the browser resources when
	// it is no longer needed
	defer cancel()

	logger.Println("Start")
	logger.Println(os.Args[1])
	logger.Println(os.Args[2])
	logger.Println(os.Args[3])

	err := chromedp.Run(ctx,
		// visit the target page
		chromedp.Navigate("https://ssu.upslp.edu.mx/ss/Home.aspx"),
		// wait for the page to load
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),
	)
	if err != nil {
		log.Fatal("Error while performing the automation logic:", err)
	}
	logger.Println("After Navigate")

	user := "//*[@id='ctl00_ucUserLogin_lvLoginUser_ucLoginUser_lcLoginUser_UserName']"
	user_env := os.Getenv("USER_ENV")
	pw := "//*[@id='ctl00_ucUserLogin_lvLoginUser_ucLoginUser_lcLoginUser_Password']"
	pw_env := os.Getenv("PW_ENV")
	accessbtn := "//*[@id='ctl00_ucUserLogin_lvLoginUser_ucLoginUser_lcLoginUser_LoginButton']"
	class := "//*[@id='tabNav']/li[4]/a"
	grades := "//*[@id='subNavDefault']/li[3]/a"
	group_input := os.Args[2]
	group_selector := "//a[contains(text(),'" + group_input + "') and contains(@class, 'arrowLink')]"
	logger.Println(group_selector)
	attendance := "//*[@id='newLeftNav']/li[4]/a"
	tag_xpath := "//*[@id='activitygrades']/div[2]/div[2]/span[2]"
	day_input := os.Args[1]
	day_selector := "//a[contains(text(),'" + day_input + "')]"
	logger.Println(day_selector)

	attendance_general := `//*[@id="ctl00_mainContentZone_AttendanceList_MeetingAttendStatusDropDown"]`
	logger.Println(attendance_general)

	apply_status := `//*[@id="ctl00_mainContentZone_AttendanceList_BatchCreateButton"]`
	save_attendance := `//*[@id="ctl00_mainContentZone_AttendanceList_ByMeetingSaveButton"]`

	students := strings.Split(os.Args[3], ",")
	logger.Println(students)
	//student := "//*[@id="dailyAttendance"]/table/tbody/tr[17]/td[2]"
	//drop_box := "//*[@id="ddlbDailyAttendance15485630"]"
	//atendande_true//*[@id="ddlbDailyAttendance15485630"]/option[3]
	//attendance_false//*[@id="ddlbDailyAttendance15485630"]/option[4]

	var id string
	var group string
	var tag string
	var day_output string
	var student_name string

	err1 := chromedp.Run(ctx,
		chromedp.SendKeys(user, user_env),
		//chromedp.Sleep(1*time.Second),

		chromedp.SendKeys(pw, pw_env),
		//chromedp.Sleep(1*time.Second),

		chromedp.Click(accessbtn),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		chromedp.Click(class, chromedp.BySearch),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		chromedp.Click(grades),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		chromedp.Text("//*[@id='ctl00_ucHeader_ucWelcomeUser_welcomeUser']/span", &id),
		chromedp.Text(group_selector, &group),
		chromedp.Click(group_selector, chromedp.BySearch),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		chromedp.Click("//a[contains(text(), '1er Parcial')]", chromedp.BySearch),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		chromedp.Text("//td[contains(text(), '000-18-2394')]/preceding-sibling::td[@style]", &student_name),
		// TODO: get all students ids
		// //table[@id='assignmentTable']/tbody/tr[not (@style) and not(@class='trTableHeader')]

		chromedp.Click(attendance),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		chromedp.Text(tag_xpath, &tag),

		chromedp.Text(day_selector, &day_output),
		chromedp.Click(day_selector),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		// set general attendance true, then update individual false
		chromedp.SetValue(attendance_general, "13", chromedp.BySearch),
		chromedp.Click(apply_status),
		chromedp.Click(save_attendance),
		chromedp.WaitVisible("//div[@id = 'footer']", chromedp.BySearch),

		// select no attendance students

		// chromedp.Value(`#example-After textarea`, &example),
	)
	if err1 != nil {
		log.Fatal("Error:", err1)
	}
	logger.Println(id)
	logger.Println(group)
	logger.Println(tag)
	logger.Println(day_output)
	logger.Println(student_name)
	logger.Println("End")

}
