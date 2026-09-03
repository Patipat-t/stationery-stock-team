# TEAM_CHARTER.md

## สมาชิกและบทบาท

| ลำดับ | รหัสนักศึกษา | ชื่อ - นามสกุล | GitHub Username | บทบาท |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 67332110028-1 | ปฏิพัทธ์ | @Patipat-t | Product Owner / Developer |
| 2 | 67332110255-2 | ศิริโรจน์ | @sirirotkaphon1 | Scrum Master / Developer |
| 3 | 67332110275-8 | สรวิชญ์ | @sorawitmm-sudo | Developer |
| 4 | 67332110260-0 | ชลธิชา | @cholthichasu-stack | Developer |
| 5 | 67332110217-1 | สุรวัจน์ | @surawatch | Developer |

## Branching Strategy

ทีมใช้ GitHub Flow:
- main branch ต้อง deploy ได้เสมอ ห้าม commit โดยตรง
- ทุก feature ใหม่ต้องสร้าง branch ชื่อ feat/<issue-number>-<short-name>
- ทุก PR ต้องมีคนอื่นในทีมอย่างน้อย 1 คน review และ approve ก่อน merge

## เพดานงานที่ทำพร้อมกัน (WIP limit)

- คอลัมน์ In Progress มีการ์ดพร้อมกันได้ไม่เกิน 5 ใบ (เริ่มที่จำนวนคนที่เขียนโค้ดในทีม)
- เมื่อชนเพดาน ห้ามลากการ์ดใหม่เข้ามา ให้ช่วยกันปิดของเดิมหรือรีวิว PR ที่ค้างใน In Review ก่อน
- ปรับเพดานระหว่าง sprint ได้ แต่ต้องเขียนเหตุผลกำกับไว้ท้ายหัวข้อนี้ ไม่ใช่ปรับเพราะการ์ดล้น

## Sprint Goal (Sprint 1)

sprint นี้ทีมจะส่งมอบ US-01, US-02, US-03 และ US-04 ที่รันได้จริงและผ่าน acceptance criteria ครบ

## AI Usage Policy

- ใช้ AI ช่วยเขียน draft code และ draft commit message ได้
- ทุก commit message ที่ AI generate ต้องอ่านและแก้ให้ตรงกับ diff จริงก่อน commit
- ห้าม copy code จาก AI โดยไม่อ่านและทำความเข้าใจก่อน
- ใช้เฉพาะ AI ที่ไม่มีค่าใช้จ่าย ไม่บังคับซื้อ subscription
