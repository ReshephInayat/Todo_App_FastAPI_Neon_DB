import { baseUrl } from "@/lib/const";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();
  console.log("BODY: ", body);

  const url = baseUrl();

  const data = {
    content: body.content,
  };

  const res = await fetch(`${url}/todos/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    cache: "no-store",
  });

  console.log("Got a post request", res.status, res.statusText);

  return NextResponse.json(res);
}
