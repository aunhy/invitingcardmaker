// ============================================================
// ✏️  여기만 바꾸면 새 초대장 완성!
// ============================================================

const EVENT_CONFIG = {

  // 행사 고유 ID (Sheets에서 구분용, 영문+숫자만)
  event_id: "byebyekin",

  // 상단 타이틀 & 서브타이틀
  title: "퇴사는 핑계일 뿐",
  subtitle: "오랜만에 모여서 맛있는 거 먹기",

  // 날짜 & 시간 표시 문구
  date: "5월 22일 금요일",
  time: "18:30 PM",

  // 초대 본문 (줄바꿈은 \n)
  description: "마지막 남은 장터즈, **현아 승훈** 드디어 킨텍스 떠납니다! ✈️\n가기 전에 다 같이 모여 맛있는 거 먹어요. 😋\n**즐거운 마음으로! 함께 해주시면 감사하겠습니다!**\n\n2차, 3차는 자유롭게! 부담 갖지 말고 편하게 참석해주세요. :)",

  // 회신 마감
  deadline: "5월 18일 15시",

  // 예약명
  reservation_name: "최승훈",

  // 장소 목록 (최대 제한 없음, 원하는 만큼 추가/삭제)
  venues: [
    {
      round: "1차",
      name: "맛있는 왕소금구이",
      map_url: "https://naver.me/xAFCYCYF",
      description: "회식의 꽃은 고기. 꽃삼겹살 & 꽃목살",
      tip: { author: "자엽 대리님", text: "여기 잔치국수 맛있어요" },
      warning: null,
    },
    {
      round: "2차",
      name: "치킨더멤버",
      map_url: "https://naver.me/GV2LKgD2",
      description: "옛날식치킨 🍗 다양한 맛을 먹어보겠어요 (*감튀있음)",
      tip: null,
      warning: "기름 냄새 주의! (옷에 기름냄새 엄청 뱁니다..!)",
    },
    {
      round: "3차",
      name: "호맥 (HOMAC)",
      map_url: "https://naver.me/5KbMx4wD",
      description: "시원한 맥주와 호떡! 분모자 떡볶이도 맛있음 (*샤베트 있음)",
      tip: { author: "장터즈", text: "저희의 새로운 방앗간이에요." },
      warning: null,
    },
  ],

  // 참석 옵션 (value는 DB에 저장되는 값, label은 화면에 표시)
  rsvp_options: [
    { value: "from1", label: "1차부터 참석 🙋" },
    { value: "from2", label: "2차부터 합류 🕐" },
    { value: "no",    label: "불참 (마음만 함께) 😢" },
  ],

  // Google Apps Script 배포 URL (배포 후 여기 붙여넣기)
  gas_url: "https://script.google.com/macros/s/AKfycbznckIfcljYqHBy39mh2FI1_feVVtMaECSGOhaRZFOQDNYss1LI5kYy25hYE45aBNx5/exec",
};
