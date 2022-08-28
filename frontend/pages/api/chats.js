export default function handler(req, res) {
    res.status(200).json([
      { 
        id: 1,
        name: 'Derrick',
        content: 'Hey everyone, I just made this library, hope everyone likes it!', 
      },
      {
        id: 2,
        name: 'Kevin',
        content: 'yo this is sickkkk'
      },
      {
        id: 3,
        name: 'Travis',
        content: 'yeye boi'
      },
      {
        id: 4,
        name: 'Elon',
        content: 'I like Mars'
      },
      {
        id: 5,
        name: 'Jeff',
        content: 'I like Money'
      },
      {
        id: 6,
        name: 'yeye',
        content: 'sdsiudhas'
      }
  
    ])
  }
  