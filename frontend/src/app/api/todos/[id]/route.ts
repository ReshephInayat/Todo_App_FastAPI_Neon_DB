import { baseUrl } from "@/lib/const";
import { revalidatePath, revalidateTag } from "next/cache";
import { NextRequest, NextResponse } from "next/server";

interface Props {
  params: {
    id: string;
  };
}

export async function DELETE(req: NextRequest, { params }: Props) {
  const { id } = params;
  const url = baseUrl();

  const res = await fetch(`${url}/todos/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  console.log("Got a Delete request", res.status, res.statusText);

  revalidatePath("/");
  revalidateTag("todos");

  return NextResponse.json(res);
}
