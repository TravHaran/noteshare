// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default function handler(req, res) {
  res.status(200).json([
    { 
    id: 1,
    name: 'title1',
    description: 'description 1', 
    },
    {
      id: 2,
      name: 'title2',
      description: 'description 2'
    }

  ])
}
