import prisma from "@/db";

export async function GET(request: Request) {
  const homer = await prisma.male.create({
    include: { person: true },
    data: { person: { create: { firstName: "Homer", lastName: "Simpson" } } },
  });
  const marge = await prisma.female.create({
    include: { person: true },
    data: { person: { create: { firstName: "Marge", lastName: "Bouvier" } } },
  });
  const bart = await prisma.male.create({
    include: { person: true },
    data: {
      person: { create: { firstName: "Bart", lastName: "Simpson" } },
      father: { connect: { id: homer.id } },
      mother: { connect: { id: marge.id } },
    },
  });
  const lisa = await prisma.female.create({
    include: { person: true },
    data: {
      person: { create: { firstName: "Lisa", lastName: "Simpson" } },
      father: { connect: { id: homer.id } },
      mother: { connect: { id: marge.id } },
    },
  });

  return Response.json([homer, marge, bart, lisa]);
}
